from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.models import Profile

UserModel = get_user_model()
class ProfileTest(TestCase):

    def test_if_first_OR_last_name_contains_only_letter__expect_to_fail(self):
        UserModel.objects.create_user(
            username='serhan',
            password='123456',

        )
        USER_DATA = {
            'first_name': 'Serhan',
            'last_name': 'Yı3lmaz',
            'picture': 'https://picture.io',
            'user':UserModel.objects.get(username='serhan'),
        }
        profile = Profile(**USER_DATA)
        with self.assertRaises(ValidationError) as ex:
            profile.full_clean()
            profile.save()
        self.assertIsNotNone(ex.exception)

    def test_if_it_prints_first_name_and_last_name_corectly_expect_to_Succeed(self):
        UserModel.objects.create_user(
            username='serhan',
            password='123456',

        )
        USER_DATA = {
            'first_name': 'Serhan',
            'last_name': 'Yılmaz',
            'picture': 'https://picture.io',
            'user': UserModel.objects.get(username='serhan'),
        }
        profile = Profile(**USER_DATA)
        self.assertEqual('Serhan Yılmaz Profile', str(profile))