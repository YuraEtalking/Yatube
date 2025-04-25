"""Модуль содержит кастомные поля для сериализаторов."""
from typing import Union

import base64

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    """Кастомный тип поля ImageField для изображений в формате base64."""

    def to_internal_value(self, data: Union[str, ContentFile]) -> ContentFile:
        """Преобразует строку с изображением base64 в ContentFile."""
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)
