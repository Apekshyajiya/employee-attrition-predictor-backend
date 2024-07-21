from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password=None, **extra_fields):
        if not email:
            raise ValueError('The email is needed')
        email =self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.create_user(email,password, **extra_fields)
    
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
        email = models.EmailField(unique=True)
        username = models.CharField(max_length=150)
        name = models.CharField(max_length=150)
        age = models.PositiveIntegerField()
        years_of_exp = models.PositiveBigIntegerField(null=True, blank=True)
        profile_pic = models.ImageField(null=True, blank=True)
        joined = models.DateTimeField(auto_now_add=True)
        updated = models.DateTimeField(auto_now=True)
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=False)

        objects = CustomUserManager()

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['username']

        def __str__(self):
             return self.email
