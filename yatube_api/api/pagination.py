"""Модуль содержит кастомные классы пагинации."""
from rest_framework.pagination import LimitOffsetPagination


class PostPagination(LimitOffsetPagination):
    """Кастомный класс пагинации."""

    page_size = 10
