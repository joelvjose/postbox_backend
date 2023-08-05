from django.urls import path
from . import views
from .views import MyTokenObtainPairView,RegisterUser,RetrieveUserView,UsersList,BlockUser

from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView


urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='verify_refresh'),
    path('',views.getRoutes,name='getRoutes'),
    path('users/me/',RetrieveUserView.as_view() ,name='getRoutes'),
    path('register/',RegisterUser.as_view(),name='register'),
    path('userslist/',UsersList.as_view(), name='userslist'),
    path('blockuser/<str:id>',BlockUser.as_view(), name='blockuser'),
    
]
