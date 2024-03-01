from django import template

register = template.Library()


@register.filter(name="get_item")
def get_item(lst, ind):
    try:
        return lst[ind]
    except IndexError:
        return None



