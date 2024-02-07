import re

from django.core.exceptions import ValidationError

from .constants import FORBIDDEN_USERNAMES


def validate_username(value):

    if value.lower() in FORBIDDEN_USERNAMES:
        raise ValidationError(f"Имя пользователя не может быть '{value}'!")

    valid_username_pattern = re.compile(r'^[\w.@+-]+\Z')
    bad_characters_in_username = list(
        filter(None, valid_username_pattern.split(value))
    )

    if bad_characters_in_username:
        raise ValidationError(
            f'Недопустимые символы {bad_characters_in_username} '
            f'в имени пользователя {value}!'
        )
