from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import status 
from rest_framework.decorators import action 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Patient,Doctor,PatientDoctorMapping
from .serializers import PatientSerializer,DoctorSerializer,PatientDoctorMappingSerializer
from rest_framework.exceptions import PermissionDenied

# Create your views here.

class PatientViewSet(ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user 
        
        if user.is_staff:
            return Patient.objects.all()
        return Patient.objects.filter(created_by=user)
    
    def get_serializer_context(self):
        return {'request':self.request}
    
    


class DoctorViewSet(ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Doctor.objects.all()
        return Doctor.objects.filter(created_by=user)
    
    
# class PatientDoctorMappingViewSet(ModelViewSet):
#     queryset = PatientDoctorMapping.objects.all()
#     serializer_class = PatientDoctorMappingSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     @action(detail=False, methods=['get'], url_path=r'patient/(?P<patient_id>\d+)')
#     def get_doctors_by_patient(self, request, patient_id=None):
#         # This handles GET /api/mappings/patient/<patient_id>/
#         mappings = PatientDoctorMapping.objects.filter(patient_id=patient_id)
#         serializer = self.get_serializer(mappings, many=True)
#         return Response(serializer.data)

#     def destroy(self, request, *args, **kwargs):
#         # This handles DELETE /api/mappings/<id>/
#         return super().destroy(request, *args, **kwargs)
    
    


class PatientDoctorMappingViewSet(ModelViewSet):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete'] 

    def get_queryset(self):

        user = self.request.user
        return PatientDoctorMapping.objects.select_related('patient', 'doctor').filter(
            patient__created_by=user,
            doctor__created_by=user
        )

    def perform_create(self, serializer):
    
        patient = serializer.validated_data['patient']
        doctor = serializer.validated_data['doctor']
        if patient.created_by != self.request.user or doctor.created_by != self.request.user:
            raise PermissionDenied("You can only map your own patients and doctors.")
        serializer.save()

    @action(detail=False, methods=['get'], url_path=r'patient/(?P<patient_id>\d+)')
    def get_doctors_by_patient(self, request, patient_id=None):

        user = request.user
        mappings = PatientDoctorMapping.objects.filter(
            patient__id=patient_id,
            patient__created_by=user,
            doctor__created_by=user
        )
        serializer = self.get_serializer(mappings, many=True)
        return Response(serializer.data)
