"""Модуль разрешений."""
from typing import Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Класс разрешений.

    Предоставляет доступ на чтение всем пользователям на безопасные методы
    (GET, HEAD и OPTIONS), а доступ на изменение только владельцу объекта.
    """

    def has_object_permission(
            self,
            request: Request,
            view: APIView,
            obj: Any
    ):
        """Проверяет права доступа пользователя к конкретному объекту."""
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
