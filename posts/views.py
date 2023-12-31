from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions,status,generics

from .serializer import PostSerializer
from .models import posts
from base.models import User



class PostListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    post_queryset = posts.objects.all().exclude(is_deleted = True).order_by('-created_at')
    serializer_class = PostSerializer
    
class CreatePostView(APIView):
    permission_classes  = [permissions.IsAuthenticated]
    serializer_class    = PostSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            img = request.data['image']
            caption = request.data['caption']
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(author=user, img=img, caption=caption)
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
class DeletePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    
    def delete(self,request,pk):
        try:
            post = posts.objects.get(id=id)
            post.is_deleted=True
            post.save()
            return Response(status=status.HTTP_200_OK)
        except posts.DoesNotExist:
            return Response("No such post found.!",status=status.HTTP_404_NOT_FOUND)