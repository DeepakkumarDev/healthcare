from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response 
from .models import User 
from .serializers import UserRegisterationSerializer, UserLoginSerializer,CurrentUserSerializer,UserChangePasswordSerialzier
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserRegisterationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            'detail': 'Registration Successful',
            'tokens': tokens,
            'user': serializer.data,
        }, status=status.HTTP_201_CREATED)


class LoginViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = get_tokens_for_user(user)

        return Response({
            'detail': 'Login successful',
            'tokens': tokens,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)



class CurrentUserViewSet(ModelViewSet):
    http_method_names = ['get','put','patch','delete']
    serializer_class = CurrentUserSerializer 
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
        
    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        if self.action == 'changepassword':
            return UserChangePasswordSerialzier
        return CurrentUserSerializer


    @action(detail=False, methods=['put'], url_path='changepassword', permission_classes=[IsAuthenticated])
    def changepassword(self, request, *args, **kwargs):  
        serializer = UserChangePasswordSerialzier(instance=self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password updated successfully'}, status=status.HTTP_200_OK)
