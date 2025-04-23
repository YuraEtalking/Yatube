"""Модуль разрешений."""
from typing import Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Класс разрешений.

    Предоставляет доступ на чтение всем пользователям, а доступ на
    изменение только владельцу объекта.
    """

    def has_permission(self, request: Request, view: APIView):
        """Проверяет наличие прав доступа пользователя на уровне запроса."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(
            self,
            request: Request,
            view: APIView,
            obj: Any
    ):
        """Проверяет права доступа пользователя к конкретному объекту."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
