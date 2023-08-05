
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework import permissions,status

from .serializer import UserSerializer
from .models import User

from django.core.exceptions import ObjectDoesNotExist

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        token['email'] = user.email
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Create your views here.
@api_view(['GET'])
def getRoutes(request):
    routes = [
        'token/',
        'token/refresh',
        'api/notes/',
        'api/notes-detail/<str:pk>/',
        'api/notes-create/',
        'api/notes-update/<str:pk>/',
        'api/notes-delete/<str:pk>/'
        
    ]
    
    return Response(routes)

class RegisterUser(APIView):
    def post(self,request,format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()                      
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
class RetrieveUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = request.user
    user = UserSerializer(user)

    return Response(user.data, status=status.HTTP_200_OK)

class UsersList(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        try:
            user = User.objects.filter(is_admin = False)
            serializer = UserSerializer(user, many = True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class BlockUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request,id):
        try:
            user=User.objects.get(id=id)
            if user.is_active:
                user.is_active=False
            else:
                user.is_active=True
            user.save()
            # return Response(
                # status=status.HTTP_200_OK)
                
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)