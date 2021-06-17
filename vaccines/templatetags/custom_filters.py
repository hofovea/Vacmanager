from django import template

register = template.Library()


#  @register.filter()
# def update_variable(value):
#     value = 'False'
#     return value
#
#
# @register.simple_tag
# def is_equal(val1, val2):
#     if val1 == val2:
#         return '1'
#     else:
#         return '0'

@register.filter()
def get_life_period_string(life_period):
    if life_period == 1:
        return 'Немовля'
    elif life_period == 2:
        return 'Дитина'
    else:
        return 'Дорослий'


@register.filter()
def get_age_period_string(age_period):
    if age_period == 1:
        return '1 день'
    elif age_period == 2:
        return '2-5 днів'
    elif age_period == 3:
        return '2 місяці'
    elif age_period == 4:
        return '4 місяці'
    elif age_period == 5:
        return '6 місяців'
    elif age_period == 6:
        return '12 місяців'
    elif age_period == 7:
        return '18 місяців'
    elif age_period == 8:
        return '6 років'
    elif age_period == 9:
        return '14 років'
    elif age_period == 10:
        return '16 років'
    else:
        return 'Дорослий'
