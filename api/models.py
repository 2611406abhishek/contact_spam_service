from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(
        self, phone_number, name, password=None, email=None, **extra_fields
    ):
        if not phone_number:
            raise ValueError("Users must have a phone number")
        if not name:
            raise ValueError("Users must have a name")
        phone_number = self.normalize_email(phone_number)
        user = self.model(
            phone_number=phone_number, name=name, email=email, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, phone_number, name, password, email=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone_number, name, password, email, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=30, unique=True)
    email = models.EmailField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return f"{self.name} ({self.phone_number})"


class Contact(models.Model):
    owner = models.ForeignKey(User, related_name="contacts", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=30)

    class Meta:
        unique_together = ("owner", "phone_number")

    def __str__(self):
        return f"{self.name} ({self.phone_number}) from {self.owner.phone_number}"


class Global(models.Model):
    name = models.CharField(max_length=255)  
    email = models.EmailField(null=True, blank=True)
    phoneNumber = models.CharField(max_length=30)
    spamCount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.phoneNumber}) - Spam: {self.spamCount}"
