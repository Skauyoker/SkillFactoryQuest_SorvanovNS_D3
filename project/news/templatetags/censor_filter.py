from django import template
from django.utils.safestring import mark_safe
from django.core.exceptions import TemplateSyntaxError

register = template.Library()


@register.filter()
def censor(value, args='text'):
    """Фильтр для цензурирования слов в тексте."""
    if not isinstance(value, str):
        raise TemplateSyntaxError("Filter 'censor_words' should only be applied to string variables.")
    # Разделяем входную строку по пробелам и преобразуем в множество для уникальности
    value_words = value.split()
    # Преобразуем аргументы в множество для уникальности
    # args_words = set(args.split(','))
    args_words = [word.lower() for word in args.split(',')]

    # Создаем новый список слов, где каждое слово из args заменяется на '*'
    censored_words = [
        word if word.lower() not in args_words else word[0] + '*' * (len(word) - 1)
        for word in value_words
    ]

    # Возвращаем результат в виде строки
    return ' '.join(censored_words)
# return str(censored_words)
