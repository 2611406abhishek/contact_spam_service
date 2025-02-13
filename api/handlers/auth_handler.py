from api.managers.user_manager import UserManagerService
from api.managers.global_manager import GlobalManagerService

class AuthHandler:
    def __init__(self):
        self.user_manager = UserManagerService()
        self.global_manager = GlobalManagerService()

    def register_user(self, name, phone_number, email, password):
        if self.user_manager.exists_by_phone(phone_number):
            raise ValueError("A user with this phone number already exists.")

        user = self.user_manager.register_user(name, phone_number, email, password)
        self.global_manager.create_or_update_global(phone_number, name, email)

        return user
