from django.core.cache import cache
from api.models import Global

def get_spam_count(phone_number):
    """
    Returns the spam count for the given phone number.
    Caches the count in Redis for 60 seconds.
    """
    key = f"spam_count:{phone_number}"
    count = cache.get(key)

    if count is None:
        global_entry = Global.objects.filter(phoneNumber=phone_number).first()
        count = global_entry.spamCount if global_entry else 0 
        cache.set(key, count, timeout=60) 
    
    return count
