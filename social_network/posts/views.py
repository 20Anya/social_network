from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from posts.models import Post, Like, Comment
from posts.serializers import PostSerializer, CommentSerializer
from posts.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для поста."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated(), IsOwnerOrReadOnly()]

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return []

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментария."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated(), IsOwnerOrReadOnly()]

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return []

    def perform_create(self, serializer):
        """ Метод создания комментария в посте. """
        serializer.save(post_id=self.kwargs['post_id'],
                        author=self.request.user)

class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        """ Метод создания лайка в посте. """
        post = Post.objects.get(id=post_id)
        if not Like.objects.filter(post=post, author=request.user).exists():
            Like.objects.create(post=post, author=request.user)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        """ Метод удаления лайка в посте. """
        post = Post.objects.get(id=post_id)
        if Like.objects.filter(post=post, author=request.user).exists():
            Like.objects.filter(post=post, author=request.user).delete()
        return Response(status=status.HTTP_200_OK)