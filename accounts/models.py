from django.core.validators import *

# Create your models here.
from django.contrib.auth import models as auth_models, get_user_model
from django.contrib.auth.models import User
from django.db import models

from accounts.manager import PetStagramUserManager
from common.validators import only_letters_validator


# Create your models here.

class PetStagramUser(auth_models.AbstractBaseUser,auth_models.PermissionsMixin):
    USERNAME_MAX_LENGTH=30
    username = models.CharField(
        unique=True,
        null=False,
        blank=False,
        max_length=USERNAME_MAX_LENGTH
    )
    is_staff = models.BooleanField(
        default=False
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    USERNAME_FIELD = 'username'
    objects = PetStagramUserManager()

class Profile(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = 'Do not show'
    GENDERS = [(x,x) for x in (MALE,FEMALE,DO_NOT_SHOW)]
    FIRST_NAME_MAX_LENGHT=30
    LAST_NAME_MAX_LENGHT = 30
    FIRST_NAME_MIN_LENGHT = 2
    LAST_NAME_MIN_LENGHT = 2
    first_name = models.CharField(max_length=FIRST_NAME_MAX_LENGHT,
                                  validators=[
                                      MinLengthValidator(FIRST_NAME_MIN_LENGHT,'first name must be between 2 and 30'),
                                      only_letters_validator],
                                  )
    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGHT,
        validators=[
            MinLengthValidator(LAST_NAME_MIN_LENGHT, 'last name must be between 2 and 30'),
            only_letters_validator,
        ],
    )
    picture = models.URLField()
    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    email = models.EmailField(
        null=True,
        blank=True,
    )
    gender = models.CharField(
        max_length=max(len(gender) for gender,_ in GENDERS),
        null=True,
        blank=True,
        choices=GENDERS,
        default=DO_NOT_SHOW,
    )

    user = models.OneToOneField(
        PetStagramUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} Profile"
