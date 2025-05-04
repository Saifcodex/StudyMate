from django import template
from datetime import datetime

register = template.Library()

@register.filter
def format_time_string(value):
    """
    Convert 'HH:MM:SS' string to 'hh:mm AM/PM' format.
    """
    try:
        time_obj = datetime.strptime(value, "%H:%M:%S")
        return time_obj.strftime("%I:%M %p")
    except:
        return value  # Fallback in case format is wrong
