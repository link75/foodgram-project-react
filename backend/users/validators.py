import re

from django.core.exceptions import ValidationError

from .constants import FORBIDDEN_USERNAMES


def validate_username(username):
    if username.lower() in FORBIDDEN_USERNAMES:
        raise ValidationError(
            f'Данное имя ({FORBIDDEN_USERNAMES}) нельзя использовать. '
            f'Придумайте другое имя!'
        )
    if not bool(re.match(r'^[\w.@+-]+\Z', username)):
        raise ValidationError(
            'Имя пользователя содержить запрещенные символы. Разрешено '
            'использовать только буквы, цифры и символы @/./+/-/.'
        )
    return username
