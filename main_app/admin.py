

from django.contrib import admin

from accounts.models import Profile
from main_app.models import  Pet, PetPhoto


# Register your models here.

class PetInlineAdmin(admin.StackedInline):
    model = Pet



@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name','type']

@admin.register(PetPhoto)
class PetPhotoAdmin(admin.ModelAdmin):
    pass
