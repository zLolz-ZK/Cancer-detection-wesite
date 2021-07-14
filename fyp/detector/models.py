#from typing_extensions import Required
import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from image_cropping import ImageCropField, ImageRatioField


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)


    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user



gender_choices = (
    ('NA', "NA"),
    ('M',"Male"),
    ('F', "Female"),
)

class Doctor(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(null=False,unique=True)
    username = models.CharField(max_length=150, unique=True)
    fname = models.CharField(max_length=20, blank=False, )
    lname = models.CharField(max_length=20, blank=False, )
    #password = models.CharField(max_length=50, null=False)
    created = models.DateTimeField(default=timezone.now)
    hospital_name = models.CharField(max_length=100, blank=False, )
    
    dob = models.DateField(blank=True, default=timezone.now)
    designation = models.CharField(max_length=30, blank=False, )
    gender = models.CharField(max_length=2,
            choices = gender_choices,
            default='?')
    mob_no = models.CharField(blank=True,max_length=10,)

    is_valid = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now_add=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_age(self):
        today = datetime.date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        
    def __str__(self):
        return f'{self.username}'


class Patient(models.Model):
    patient_id = models.SlugField(null=False, unique=True, max_length=50)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False)
    fname = models.CharField(max_length=30, blank=False)
    lname = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(default=timezone.now)

    email_id = models.EmailField(unique=True,null=True,blank=True, max_length=50) 
    dob = models.DateField(null=True,)
    gender = models.CharField(max_length=2,
            choices = gender_choices,
            default='NA')
    
    symptoms = models.TextField(max_length=100,null=True)
    mob_no = models.CharField(null=True,max_length=10,blank=True)
    weight = models.FloatField(null=True,blank=True)
    height = models.FloatField(null=True,blank=True)
    family_history = models.CharField(null=True,max_length=30,blank=True)
    allergies = models.CharField(null=True,max_length=30,blank=True)
    products_used = models.CharField(null=True,max_length=30,blank=True)
    previous_record = models.CharField(null=True,max_length=30,blank=True)



    image = models.ImageField(null=True,upload_to='images/',blank=True)
    img = ImageCropField(upload_to='images/',blank=False)
    cropping = ImageRatioField('img', '299x299', size_warning=True,free_crop=True)
    result = models.CharField(null=True,max_length=30,blank=True)
    accuracy = models.FloatField(null=True,blank=True)
    feedback = models.TextField(max_length=200, null=True, blank=True)
    

    def __str__(self):
        return f"{self.doctor}'s patient {self.fname} {self.lname}"

    def get_age(self):
        today = datetime.date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

# Create your models here.
class DeepClassifier(models.Model):
    name = models.CharField(max_length=20)
    moel_type = models.CharField(max_length=20)
    desc = models.CharField(max_length=100)
    class_names = ArrayField(
            models.CharField(max_length=10, blank=True),
            #size=8,
        ) 

class SomeImage(models.Model):
    image = ImageCropField(blank=True, upload_to='uploaded_images',)
    # size is "width x height"
    cropping = ImageRatioField('image', '430x360', size_warning=True,free_crop=True)

