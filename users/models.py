from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from django.forms import DateField
from django.http import request
from datetime import datetime
from datetime import timedelta
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email,FirstName=None,LastName=None,typee=None,Province=None,District=None,Sector=None,Cell=None,phone=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users must have a valid email')
        if not phone:
            raise ValueError('Users must have a valid phone number')
        if not password:
            raise ValueError("You must enter a password")

        email = self.normalize_email(email)
        user_obj = self.model(email=email)
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.FirstName = FirstName
        user_obj.LastName = LastName
        user_obj.District = District
        user_obj.Sector = Sector
        user_obj.Province = Province
        user_obj.Cell = Cell
        user_obj.phone = phone
        user_obj.typee = typee  
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email,FirstName=None,LastName=None,Province=None,District=None,typee=None,Sector=None,Cell=None, phone=None, password=None):
        user = self.create_user(
            email,FirstName=FirstName,LastName=LastName,District=District,Province=Province,Sector=Sector,typee=typee,Cell=Cell,phone=phone, password=password, is_staff=True)
        return user

    def create_superuser(self, email,FirstName=None,LastName=None,District=None,Sector=None, phone=None, password=None):
        user = self.create_user(email,FirstName='Super',LastName='Admin',District="District",Sector="Sector", phone='0787018287',Province="Nyaruguru",
                                password=password, is_staff=True, is_admin=True)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    FirstName=models.CharField(max_length=255,  null=True, blank=True)
    LastName=models.CharField(max_length=255,  null=True, blank=True)
    District=models.CharField(max_length=255,  null=True, blank=True)
    Sector=models.CharField(max_length=255,  null=True, blank=True)
    Cell=models.CharField(max_length=255,  null=True, blank=True)
    Province=models.CharField(max_length=255,  null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, unique=True, null=True, blank=True)
    typee = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.typee +" "+ self.Sector

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Case(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, null=True, blank=True)
    Message = models.CharField(max_length=250,blank=True,null=True)
    Sector = models.CharField(max_length=250,blank=True,null=True)
    symptoms = models.CharField(max_length=250,blank=True,null=True)
    cattleType = models.CharField(max_length=250,blank=True,null=True)
    image = models.ImageField(null=True, blank=True)
    reply = models.TextField(blank=True, null=True,
                             default="None")
    replied = models.BooleanField(default=False)
    send_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Sector

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Message(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, null=True, blank=True)
    Message = models.CharField(max_length=250,blank=True,null=True)
    Sector = models.CharField(max_length=250,blank=True,null=True)
    reply = models.TextField(blank=True, null=True,
                             default="None")
    replied = models.BooleanField(default=False)
    send_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Sector