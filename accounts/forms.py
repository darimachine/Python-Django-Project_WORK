import datetime

from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.core.exceptions import ValidationError
from django.views.generic import UpdateView

from accounts.models import Profile
from common.helpers import BootstrapFormMixin

from main_app.models import PetPhoto

UserModel = get_user_model()
class CreateProfileForm(BootstrapFormMixin, auth_forms.UserCreationForm):
    first_name=forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGHT
    )
    last_name=forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGHT
    )
    picture=forms.URLField()
    date_of_birth=forms.DateField(
        widget=forms.DateInput(
            attrs={
                    'type': 'date',
                    'min': '1920-01-01',
                    'max': datetime.date.today()
                }
        )
    )
    description=forms.CharField(
        widget=forms.Textarea
    )
    email=forms.EmailField()
    gender=forms.ChoiceField(
        choices=Profile.GENDERS
    )
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._init_bootstrap_form_controls()
    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            picture=self.cleaned_data['picture'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            description=self.cleaned_data['description'],
            email=self.cleaned_data['email'],
            gender=self.cleaned_data['gender'],
            user=user)
        if commit:
            profile.save()
        return user
    class Meta:
        model=UserModel
        fields = ('username','password1','password2','first_name','last_name','picture')

class EditProfileForm(BootstrapFormMixin,forms.ModelForm):
    username = forms.CharField(
        max_length=UserModel.USERNAME_MAX_LENGTH
    )
    MIN_DATE_OF_BIRTH = datetime.date(1920, 1, 1)
    MAX_DATE_OF_BIRTH = datetime.date.today()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self.initial['gender'] = Profile.DO_NOT_SHOW
        user = self.instance.user
        self.initial['username'] = user.username

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth<self.MIN_DATE_OF_BIRTH or self.MAX_DATE_OF_BIRTH<date_of_birth:
            raise ValidationError(
                f"Date of birth must be between {self.MIN_DATE_OF_BIRTH} and {self.MAX_DATE_OF_BIRTH}"
            )
        return date_of_birth
    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.date_of_birth = self.cleaned_data['date_of_birth']
        profile.user.username = self.cleaned_data['username']
        if commit:
            profile.save()
            self.instance.user.save()
        return profile
    class Meta:
        model = Profile
        fields=('username', 'first_name', 'last_name', 'picture', 'date_of_birth', 'description', 'email', 'gender')
    #     widgets = {
    #         'first_name': forms.TextInput(
    #             attrs={
    #                 'placeholder': 'Enter first name'
    #             }),
    #         'last_name': forms.TextInput(
    #             attrs={
    #                 'placeholder': 'Enter last name'
    #             }),
    #         'picture': forms.TextInput(
    #             attrs={
    #                 'placeholder': 'Enter URL'
    #             }),
    #         'email':forms.EmailInput(
    #             attrs={
    #                 'placeholder':'Enter email'
    #             }),
    #         'description':forms.Textarea(
    #             attrs={
    #                 'placeholder':'Enter description',
    #                 'rows':3,
    #             }),
    #         'date_of_birth':forms.DateInput(
    #             attrs={
    #                 'type':'date',
    #                 'min':'1920-01-01',
    #                 'max':datetime.date.today()
    #             }
    #         )
    #
    #
    #     }
class DeleteProfileForm(forms.ModelForm):

    def save(self, commit=True):
        pets = self.instance.pet_set.all() # self.instance e PROFILA
        #should be done with signals
        PetPhoto.objects.filter(tagged_pets__in=pets).delete()
        self.instance.delete()

        return self.instance
    class Meta:
        model = Profile
        fields = ()