# Create your models here.
import datetime

from django.contrib.auth import get_user_model
from django.db import models
from common.validators import ValidateFileMaxSizeInMB

UserModel = get_user_model()
# Create your models here.

class Pet(models.Model):
    #Constans
    NAME_MAX_LENGHT=30
    CAT = 'Cat'
    DOG = 'Dog'
    BUNNY = 'Bunny'
    PARROT = 'Parrot'
    FISH='Fish'
    OTHER = 'Other'
    TYPES=[(x,x) for x in (CAT,DOG,BUNNY,PARROT,FISH,OTHER)]

    #Columns
    name =models.CharField(
        max_length=NAME_MAX_LENGHT,

    )
    type = models.CharField(
        max_length=max(len(type) for (type,_) in TYPES),
        choices=TYPES,

    )
    #optional
    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )
    #One-to-one Relation

    # One-to-many Relations

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    # Many-to_many Relations

    #Properties
    @property
    def age(self):
        if self.date_of_birth:
            return datetime.datetime.now().year-self.date_of_birth.year
        return None
    #Methods

    #dunder methods
    def __str__(self):
        return f'{self.name}'
    #Meta

    class Meta:
        unique_together=('user','name')



class PetPhoto(models.Model):
    photo = models.ImageField(
        validators=(
            ValidateFileMaxSizeInMB(5),
        )
    )
    tagged_pets = models.ManyToManyField(
        Pet,
        #validators=[atleastOnePet]
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    date_of_publication = models.DateTimeField(
        auto_now_add=True
    )
    likes = models.IntegerField(
        default=0
    )
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    def __str__(self):
        return f"Photo on {self.tagged_pets.name}"
