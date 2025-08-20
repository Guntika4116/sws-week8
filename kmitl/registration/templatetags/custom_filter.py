from django import template

register = template.Library()

@register.filter
def sortSectionByDayOfWeek(sections):
    for section in sections:
        section.day_of_week_num = section.dayOfWeek()
    return sections

@register.filter
def formatPhoneNumber(number):
    number = str(number)
    if len(number) == 10 :
        return f"{number[0:3]}-{number[3:6]}-{number[6:]}"
    return number