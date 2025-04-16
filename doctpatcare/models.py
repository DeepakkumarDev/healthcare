from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

class Patient(models.Model):
    GENDER_CHOICES_MALE = 'M'
    GENDER_CHOICES_FEMALE = 'F'
    GENDER_CHOICES_OTHER = 'O'
    GENDER_CHOICES =[
        (GENDER_CHOICES_MALE,'Male'),
        (GENDER_CHOICES_FEMALE,'Female'),
        (GENDER_CHOICES_OTHER,'Other')
        
    ]
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default=GENDER_CHOICES_OTHER)
    address = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name='patients')
    
    def __str__(self):
        return self.name 


def get_department_choices():
    return [
        ('CARD', 'Cardiology'),
        ('NEUR', 'Neurology'),
        ('ORTH', 'Orthopedics'),
        ('DERM', 'Dermatology'),
        ('PED', 'Pediatrics'),
        ('GENM', 'General Medicine'),
        ('GPHY', 'General Physician'),
        ('ENT', 'Ear, Nose, and Throat'),
        ('PSYC', 'Psychiatry'),
        ('UROL', 'Urology'),
        ('GAST', 'Gastroenterology'),
        ('ENDO', 'Endocrinology'),
        ('ONCO', 'Oncology'),
        ('NEPH', 'Nephrology'),
        ('PULM', 'Pulmonology'),
        ('SURG', 'Surgery'),
    ]


class Doctor(models.Model):
    GENDER_CHOICES_MALE = 'M'
    GENDER_CHOICES_FEMALE = 'F'
    GENDER_CHOICES_OTHER = 'O'
    GENDER_CHOICES =[
        (GENDER_CHOICES_MALE,'Male'),
        (GENDER_CHOICES_FEMALE,'Female'),
        (GENDER_CHOICES_OTHER,'Other')
        
    ]
    DEPARTMENT_CHOICES = get_department_choices()
    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    department = models.CharField(max_length=4, choices=DEPARTMENT_CHOICES)
    phone = models.CharField(max_length=15)
    birth_date = models.DateField(blank=True,null=True)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default=GENDER_CHOICES_OTHER)
    address = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='doctors')
    
    def __str__(self):
        return f"{self.name} Dept:{self.department}" 
 
    class Meta:
        unique_together = ('email', 'department', 'created_by')   
    

class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('patient', 'doctor')
    
    
    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name}"
