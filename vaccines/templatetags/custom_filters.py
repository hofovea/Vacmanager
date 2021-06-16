from django import template

register = template.Library()


# @register.filter()
def update_variable(value):
    value = 'False'
    return value


@register.simple_tag
def is_equal(val1, val2):
    if val1 == val2:
        return '1'
    else:
        return '0'


register.filter('update_variable', update_variable)
