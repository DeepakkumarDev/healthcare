from django.urls import path,include
from rest_framework_nested import routers
from .import views 



router = routers.DefaultRouter()
router.register('register',views.UserRegistrationViewSet,basename='register')
router.register('login',views.LoginViewSet,basename='login')
router.register('users',views.CurrentUserViewSet,basename='users')


urlpatterns = router.urls 
