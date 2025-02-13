from api.managers.user_manager import UserManagerService
from api.managers.contact_manager import ContactManagerService
from api.managers.global_manager import GlobalManagerService

class DetailHandler:
    def __init__(self):
        self.user_manager = UserManagerService()
        self.contact_manager = ContactManagerService()
        self.global_manager = GlobalManagerService()
    
    def get_contact_details(self, contact_id, requesting_user):
        """
        Fetch full details for a Contact by phone number from the Global database.
        If the person is a registered user, include the email only if the requesting user is in their contact list.
        """
        global_contact_record = self.global_manager.get_global_by_id(contact_id)
       
        if not global_contact_record:
            return None
        
        res = {
            "id": global_contact_record.id,
            "name": global_contact_record.name or "Unknown Number",
            "phone_number": global_contact_record.phoneNumber,
            "spam_likelihood": global_contact_record.spamCount,
        }
        user = self.user_manager.get_user_by_phone(global_contact_record.phoneNumber)
        if user:
            contacts = self.contact_manager.get_contacts_by_owner(user)
            if contacts.filter(phone_number=requesting_user.phone_number).exists() and user.email:
                res["email"] = user.email
           

        return res
