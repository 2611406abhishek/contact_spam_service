from api.managers.global_manager import GlobalManagerService

class SpamHandler:
    def __init__(self):
        self.global_manager = GlobalManagerService()
    
    def mark_number_as_spam(self, phone_number, user):
        """
        Prevent a user from marking their own phone number as spam.
        """
        if user.phone_number == phone_number:
            raise ValueError("You cannot mark your own phone number as spam.")

        return self.global_manager.mark_spam(phone_number)
