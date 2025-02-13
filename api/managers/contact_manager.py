from api.models import Contact

class ContactManagerService:
    def get_contacts_by_name(self, query):
        return Contact.objects.filter(name__icontains=query)
    
    def get_contacts_by_phone(self, phone_number):
        return Contact.objects.filter(phone_number=phone_number)
    
    def get_contact_by_id(self, contact_id):
        return Contact.objects.filter(id=contact_id).first()

    def get_contacts_by_owner(self, owner):
        return Contact.objects.filter(owner=owner)
