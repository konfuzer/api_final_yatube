from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly)
from rest_framework.pagination import LimitOffsetPagination


from posts.models import Comment, Follow, Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer)


User = get_user_model()


class PostPagination(LimitOffsetPagination):
    page_size = 10


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_paginated_response(self, data):
        return super().get_paginated_response(data)

    def list(self, request, *args, **kwargs):
        if 'limit' in request.query_params or 'offset' in request.query_params:
            self.pagination_class = PostPagination
        else:
            self.pagination_class = None

        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = Follow.objects.filter(user=user)
        search_term = self.request.query_params.get('search')
        if search_term:
            queryset = queryset.filter(following__username=search_term)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        try:
            post = Post.objects.get(id=self.kwargs.get('post_id'))
        except Post.DoesNotExist:
            raise NotFound(detail="Пост не найден.")

        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
