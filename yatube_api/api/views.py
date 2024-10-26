from django.contrib.auth import get_user_model
from rest_framework import filters, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly)

from posts.models import Comment, Follow, Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer)


User = get_user_model()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

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
