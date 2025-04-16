from django.urls import path 
from rest_framework_nested import routers
from .import views

router = routers.DefaultRouter()
router.register('patients',views.PatientViewSet,basename='patients')
router.register('doctors',views.DoctorViewSet,basename='doctors')
router.register('mappings', views.PatientDoctorMappingViewSet, basename='mapping')



urlpatterns = router.urls 
