"""Модуль содержит вьюсеты для обработки запросов к API."""
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import mixins, serializers, viewsets
from rest_framework import filters

from .permissions import IsOwnerOrReadOnly
from .pagination import PostPagination
from posts.models import Comment, Group, Follow, Post
from .serializers import (
    CommentSerializer,
    GroupSerializer,
    FollowSerializer,
    PostSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки запросов к публикациям."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = PostPagination

    def perform_create(self, serializer: serializers.ModelSerializer) -> None:
        """Переопределяет метод создания публикации.

        При создании публикации устанавливает текущего пользователя как автора.
        """
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для обработки запросов, к группам."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки запросов к комментариям."""

    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_post(self) -> Post:
        """Получаем объект поста по его ID или возвращаем 404 ошибку."""
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self) -> QuerySet[Comment]:
        """Получает queryset с комментариями для конкретной публикации."""
        post = self.get_post()
        return post.comments.all()

    def perform_create(self, serializer: serializers.ModelSerializer) -> None:
        """Переопределяет метод создания комментария.

        При создании комментария автоматически:
        - устанавливает текущего пользователя как автора
        - привязывает комментарий к конкретной публикации по post_id из URL
        """
        serializer.save(
            author=self.request.user,
            post=self.get_post()
        )


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """Вьюсет для обработки запросов на подписку и получение списка подписок
    пользователя.

    Позволяет пользователю просматривать свои подписки и подписываться на
    других пользователей.
    """

    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self) -> QuerySet[Follow]:
        """Возвращает queryset с подписками текущего пользователя."""
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer: serializers.ModelSerializer) -> None:
        """Сохраняет новую подписку для текущего пользователя."""
        serializer.save(user=self.request.user)
