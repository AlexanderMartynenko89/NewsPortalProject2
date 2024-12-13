from django import template

register = template.Library()

badwords = ['редиска', 'сосиска', 'козявка']

@register.filter()
def censor(value):
    for badword in badwords:
        value = value.replace(badword[1:], '*' * len(badword[1:]))
    return value