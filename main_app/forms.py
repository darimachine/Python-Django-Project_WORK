import datetime

from django import forms
from django.core.exceptions import ValidationError

from common.helpers import DisabledFieldsFormMixin, BootstrapFormMixin
from .models import  PetPhoto, Pet




class CreatePetForm(BootstrapFormMixin,forms.ModelForm):
    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)
        self._init_bootstrap_form_controls()



    class Meta:
        model = Pet
        fields = ('name','type','date_of_birth')
        widgets={
            'name':forms.TextInput(
                attrs={
                    'placeholder':'Enter pet name'
                }),
            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': '1920-01-01',
                    'max': datetime.date.today()

                }
            )

        }

class EditPetForm(BootstrapFormMixin,forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._init_bootstrap_form_controls()


    class Meta:
        model = Pet
        fields = ('name','type','date_of_birth')
        widgets={
            'name':forms.TextInput(
                attrs={
                    'placeholder':'Enter pet name'
                }),
            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': '1920-01-01',
                    'max': datetime.date.today()

                }
            )

        }

class DeletePetForm(BootstrapFormMixin,DisabledFieldsFormMixin,forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._init_disabled_fields()
        self._init_bootstrap_form_controls()
    class Meta:
        model = Pet
        fields = ('name', 'type', 'date_of_birth')

    def save(self, commit=True):
        self.instance.delete() #self.instance e PROFILA
        return self.instance

class CreatePetPhotoForm(BootstrapFormMixin,forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._init_bootstrap_form_controls()

    def clean_tagged_pets(self):
        tagged_pets = self.cleaned_data['tagged_pets']
        if not tagged_pets:
            raise ValidationError(f"There should be atleast one pet")
        return tagged_pets

    class Meta:
        model = PetPhoto
        fields = ('photo','description','tagged_pets')
        widgets={
            'photo':forms.ClearableFileInput(
                attrs={
                    'class': 'form-control-file',
                }
               ),
            'description': forms.Textarea(
                attrs={
                    'rows':3,
                    'placeholder':'Enter description'

                }),
            # 'tagged_pets': forms.ModelMultipleChoiceField(
            #     queryset=Pet.objects.all(),
            #     widget=forms.CheckboxSelectMultiple(),
            # )

        }



class EditPetPhotoForm(BootstrapFormMixin,forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model=PetPhoto
        fields=('photo','description','tagged_pets')
        widgets = {
            'photo': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control-file',

                }
            ),
            'description': forms.Textarea(
                attrs={
                    'rows': 3,

                }),
        }


