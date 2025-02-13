from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Contact
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .cache_utils import get_spam_count  

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ('id', 'name', 'phone_number', 'email', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            name=validated_data['name'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    spam_likelihood = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'name', 'phone_number', 'email', 'spam_likelihood')
    
    def get_spam_likelihood(self, obj):
        return get_spam_count(obj.phone_number)
    
    def get_email(self, obj):
        request = self.context.get('request')
        if not obj.email or not request:
            return None
        if request.user.contacts.filter(phone_number=obj.phone_number).exists():
            return obj.email
        return None

class ContactDetailSerializer(serializers.ModelSerializer):
    spam_likelihood = serializers.SerializerMethodField()
    
    class Meta:
        model = Contact
        fields = ('id', 'name', 'phone_number', 'spam_likelihood')
    
    def get_spam_likelihood(self, obj):
        return get_spam_count(obj.phone_number)


class SearchResultSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    phone_number = serializers.CharField()
    spam_likelihood = serializers.IntegerField()
    is_registered = serializers.BooleanField()



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return {"access": data["access"]}


class SpamMarkSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=30)