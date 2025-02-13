from django.contrib.auth import get_user_model
from api.models import Contact

User = get_user_model()

class UserManagerService:
    def exists_by_phone(self, phone_number):
        return User.objects.filter(phone_number=phone_number).exists()
    
    def register_user(self, name, phone_number, email, password):
        return User.objects.create_user(
            phone_number=phone_number,
            name=name,
            email=email,
            password=password
        )
    
    def get_user_by_phone(self, phone_number):
        return User.objects.filter(phone_number=phone_number).first()
    
    def get_user_by_id(self, user_id):
        return User.objects.filter(id=user_id).first()
    
    def search_users_by_name(self, query):
        return User.objects.filter(name__icontains=query)
    
