import re

from django.core.exceptions import ValidationError


def validate_color(value):
    regex = r'^#([A-Fa-f0-9]{6})$'
    if not re.match(regex, value):
        raise ValidationError(
            'Неправильный формат цвета! '
            'Введите цветовой HEX-код в формате #RRGGBB.'
        )
