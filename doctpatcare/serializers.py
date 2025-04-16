from rest_framework import serializers 
from .models import Patient,Doctor,PatientDoctorMapping
from rest_framework.exceptions import ValidationError


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id','name','phone','age','gender','address']
        
    def create(self,validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user     
        return super().create(validated_data)
    
    
    
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id','name','email','department','phone','birth_date','gender','address']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user

        # Check for existing doctor with same email + department + created_by
        if Doctor.objects.filter(
            email=validated_data['email'],
            department=validated_data['department'],
            created_by=user
        ).exists():
            raise ValidationError("This doctor already exists for this user in this department.")

        return super().create(validated_data)



# class PatientDoctorMappingSerializer(serializers.ModelSerializer):
#     patient_name = serializers.ReadOnlyField(source='patient.name')
#     doctor_name = serializers.ReadOnlyField(source='doctor.name')

#     class Meta:
#         model = PatientDoctorMapping
#         fields = ['id', 'patient', 'patient_name', 'doctor', 'doctor_name']
        
        
        
        
class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.name')
    doctor_name = serializers.ReadOnlyField(source='doctor.name')

    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient', 'doctor', 'patient_name', 'doctor_name']  # include patient and doctor fields

    def __init__(self, *args, **kwargs):
        super(PatientDoctorMappingSerializer, self).__init__(*args, **kwargs)

        request = self.context.get('request', None)

        if request and hasattr(request, 'user'):
            user = request.user
            self.fields['patient'].queryset = Patient.objects.filter(created_by=user)
            self.fields['doctor'].queryset = Doctor.objects.filter(created_by=user)
