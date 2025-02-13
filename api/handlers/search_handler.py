from api.managers.global_manager import GlobalManagerService
from api.managers.user_manager import UserManagerService
from api.helpers.cache_helper import get_cached_value, set_cached_value

class SearchHandler:
    def __init__(self):
        self.global_manager = GlobalManagerService()
        self.user_manager = UserManagerService()
    
    def search_by_name(self, name_query):
        cache_key = f"global_search:name:{name_query.lower()}"
        cached_result = get_cached_value(cache_key)
        if cached_result is not None:
            return cached_result

        globals_qs = self.global_manager.search_by_name(name_query)
        results = []
        for record in globals_qs:
            starts_with = 1 if record.name.lower().startswith(name_query.lower()) else 0
            is_reg = True if self.user_manager.get_user_by_phone(record.phoneNumber) else False
            results.append({
                "id": record.id,
                "name": record.name,
                "phone_number": record.phoneNumber,
                "spam_likelihood": record.spamCount,
                "is_registered": is_reg,
                "starts_with": starts_with,
            })
        results.sort(key=lambda x: (-x["starts_with"], x["name"].lower()))
        set_cached_value(cache_key, results, timeout=10)
        return results

    def search_by_phone(self, phone_query):
        cache_key = f"global_search:phone:{phone_query}"
        cached_result = get_cached_value(cache_key)
        if cached_result is not None:
            return cached_result

        user = self.user_manager.get_user_by_phone(phone_query)
        if user:
            global_record = self.global_manager.get_global_by_phone(phone_query)
            result = [{
                "id": global_record.id if global_record else None,
                "name": global_record.name if global_record else user.name,
                "phone_number": phone_query,
                "spam_likelihood": global_record.spamCount if global_record else 0,
                "is_registered": True
            }]
            set_cached_value(cache_key, result, timeout=10)
            return result
        else:
            globals_qs = self.global_manager.search_by_phone(phone_query)
            results = []
            for record in globals_qs:
                results.append({
                    "id": record.id,
                    "name": record.name,
                    "phone_number": record.phoneNumber,
                    "spam_likelihood": record.spamCount,
                    "is_registered": False
                })
            set_cached_value(cache_key, results, timeout=10)
            return results
