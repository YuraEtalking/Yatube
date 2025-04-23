"""Модуль содержащий сериализаторы для API."""
from typing import Union

import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Group, Follow, Post


User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """Кастомный тип поля ImageField для изображений в формате base64."""

    def to_internal_value(self, data: Union[str, ContentFile]) -> ContentFile:
        """Преобразует строку с изображением base64 в ContentFile."""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели публикаций."""

    text = serializers.CharField(required=True)
    author = SlugRelatedField(slug_field='username', read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        """Метакласс, определяющий параметры для PostSerializer."""

        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        """Метакласс, определяющий параметры для CommentSerializer."""

        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели групп."""

    class Meta:
        """Метакласс, определяющий параметры для GroupSerializer."""

        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели подписок."""

    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        """Метакласс, определяющий параметры для FollowSerializer.

        Так же добавлен валидатор не позволяющий на уровне api создать
        уже существующую пару значений двух полей user и following.
        """

        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message="Вы уже подписаны на этого пользователя"
            )
        ]

    def validate_following(self, value):
        """Метод не позволяет подписаться на себя."""
        if value == self.context['request'].user:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя"
            )
        return value
