from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.forms import CreateProfileForm
from accounts.models import Profile

UserModel = get_user_model()

class CreateProfileTests(TestCase):
    def test_profile_form_saved_correctly(self):
        user_data={
            'username':'serhan',
            'password':'123456',

        }
        UserModel.objects.create_user(**user_data)
        forms_user_data={
            'first_name':'serhi',
            'last_name':'lasto',
            'picture':'https://picture.io' ,
            'date_of_birth':'2004-11-10' ,
            'description' :"my description",
            'email':'serhi1334@gmail.com',
            'gender':'Male',
            'user':UserModel.objects.get(username='serhan').pk,
        }
        form = CreateProfileForm(data=forms_user_data)
        self.assertTrue(form.is_valid())


