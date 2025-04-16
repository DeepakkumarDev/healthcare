from rest_framework import serializers 
from django.contrib.auth import authenticate 
from .models import User 


class UserRegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=25,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    confirm_password = serializers.CharField(
        max_length=25,
        style={'input_type': 'password'},
        write_only=True
    )
    
    class Meta:
        model = User 
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'first_name', 'last_name']
        
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Password and confirm password do not match'})
        return attrs
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user 
    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        max_length=25,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if not username or not password:
            raise serializers.ValidationError('Username and password are required')
        
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials were provided')
        
        attrs['user'] = user 
        return attrs 



class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']





class UserChangePasswordSerialzier(serializers.Serializer):
    password = serializers.CharField(max_length=15,style={'input_type':'password'},write_only=True)
    confirm_password = serializers.CharField(max_length=15,style={'input_type':'password'},write_only=True)
    
    def validate(self,attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        
        if password != confirm_password:
            raise serializers.ValidationError('Password and confirm password do not match')
        return attrs 
    
    def update(self,instance,validated_data):
        password = validated_data.get('password')
        instance.set_password(password)
        instance.save()
        return instance 
    
