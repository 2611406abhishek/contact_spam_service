from django.core.cache import cache

def get_cached_value(key):
    """Retrieve a value from the cache by key."""
    return cache.get(key)

def set_cached_value(key, value, timeout=10):
    """Set a value in the cache with the given timeout (in seconds)."""
    cache.set(key, value, timeout=timeout)

def delete_cached_value(key):
    """Delete a value from the cache."""
    cache.delete(key)
