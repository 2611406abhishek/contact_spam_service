from api.models import Global

class GlobalManagerService:
    def get_global_by_phone(self, phoneNumber):
        return Global.objects.filter(phoneNumber=phoneNumber).first()
    

    def get_global_by_id(self, global_id):
        return Global.objects.get(id=global_id)
    
    def mark_spam(self, phoneNumber):
        global_record = self.get_global_by_phone(phoneNumber)
        if global_record:
            global_record.spamCount += 1
            global_record.save()
        else:
            global_record = Global.objects.create(name="", email=None, phoneNumber=phoneNumber, spamCount=1)
        return global_record

    def get_spam_count(self, phoneNumber):
        global_record = self.get_global_by_phone(phoneNumber)
        return global_record.spamCount if global_record else 0

    def search_by_name(self, name_query):
        return Global.objects.filter(name__icontains=name_query)

    def search_by_phone(self, phone_query):
        return Global.objects.filter(phoneNumber=phone_query)
    
    def create_or_update_global(self, phoneNumber, name, email):
        """
        Create or update an entry in the Global table whenever a user registers.
        """
        global_record, created = Global.objects.update_or_create(
            phoneNumber=phoneNumber,
            defaults={"name": name, "email": email, "spamCount": 0},
        )
        return global_record
    

         
