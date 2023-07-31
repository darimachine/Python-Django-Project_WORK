from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from accounts.models import Profile
from main_app.models import PetPhoto, Pet

UserModel = get_user_model()
class ProfileDetailsViewTests(TestCase):

    VALID_USER_CREDENTIALS = {
        'username': 'test',
        'password': 'test213',
    }
    VALID_PROFILE_CREDENTIALS = {
        'first_name': 'test',
        'last_name': 'testff',
        'picture': 'https://test.picture/url.png',
        'description': 'testdassssssssss',
        'date_of_birth': '2004-04-04',
        'gender' : 'Male',
    }
    VALID_PET_DATA= {
        'name': 'Petur',
        'type': 'Cat',

    }
    def __create_second_valid_user(self):
        user = UserModel.objects.create_user(
            username= 'tewqeqwst',
            password= 'testqweqw213',
        )
        return user
    def __create_valid_user_and_profile(self):
        user = UserModel.objects.create_user(
            **self.VALID_USER_CREDENTIALS
        )
        profile = Profile.objects.create(
            **self.VALID_PROFILE_CREDENTIALS,
            user=user
        )
        return (user,profile)
    def test_when_opening_not_existing_profile__expect_404(self):
        response = self.client.get(reverse('profile', kwargs={'pk': 1}))
        self.assertEqual(404, response.status_code)

    def test_when_all_valid__Expect_correct_template(self):

        user = UserModel.objects.create_user(
            **self.VALID_USER_CREDENTIALS
        )
        profile = Profile.objects.create(
            **self.VALID_PROFILE_CREDENTIALS,
            user=user
        )
        response = self.client.get(reverse('profile', kwargs={'pk': profile.pk}))
        self.assertTemplateUsed(response, 'profile_details.html')


    def test_when_user_is_owner__Expect_is_owner_be_true(self):
        user,profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile', kwargs={'pk': profile.pk}))
        self.assertEqual(response.context['is_owner'], True)

    def test_when_owner__is_not_owner__should_be_false(self):
        user = UserModel.objects.create_user(
            **self.VALID_USER_CREDENTIALS
        )
        user_data = {
            'username': 'test21312',
            'password': 'test213aadsa'
        }
        user2 = UserModel.objects.create_user(
            **user_data
        )
        profile = Profile.objects.create(
            **self.VALID_PROFILE_CREDENTIALS,
            user=user
        )

        self.client.login(**user_data)
        response = self.client.get(reverse('profile', kwargs={'pk': profile.pk}))
        self.assertEqual(response.context['is_owner'], False)
    def test_when_no_photo_likes__Expect_totallikescount_to_be_0(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse('profile', kwargs={'pk': profile.pk}))
        self.assertEqual(response.context['total_likes_count'], 0)

    def test_when_is_there_more_than_one_photo_likes__Expect_totalLikesCount_to_be_more_than_0(self):
        user, profile = self.__create_valid_user_and_profile()
        pet = Pet.objects.create(
            **self.VALID_PET_DATA,
            user=user,
        )
        pet_photo = PetPhoto.objects.create(
            photo='https://test.picture/url.png',
            likes=1,
            user=user,
        )
        pet_photo.tagged_pets.add(pet)
        pet_photo.save()
        response = self.client.get(reverse('profile', kwargs={'pk': profile.pk}))
        self.assertGreater(response.context['total_likes_count'], 0)
    def test_when_there_is_no_created_Photo__Expect_total_images_count_to_be_zero(self):
        user, profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse('profile', kwargs={'pk': profile.pk}))
        self.assertEqual(response.context['total_images_count'], 0)

    def test_when_there_is_a_created_Photo__Expect_total_images_count_to_be_more_than_0(self):
        user, profile = self.__create_valid_user_and_profile()
        pet = Pet.objects.create(
            **self.VALID_PET_DATA,
            user=user,
        )
        pet_photo = PetPhoto.objects.create(
            photo='https://test.picture/url.png',
            likes=0,
            user=user,
        )
        pet_photo.tagged_pets.add(pet)
        pet_photo.save()
        response = self.client.get(reverse('profile', kwargs={'pk': profile.pk}))
        self.assertGreater(response.context['total_images_count'], 0)
    def test_when_pets_are_get__Expect_to_get_pets_which_is_on_specific_owner(self):
        user, profile = self.__create_valid_user_and_profile()
        user2 = self.__create_second_valid_user()
        pet1 = Pet.objects.create(
            **self.VALID_PET_DATA,
            user=user,
        )
        pet1.save()
        pet2 = Pet.objects.create(
            name='Gosho',
            type='Dog',
            user=user2
        )
        pet2.save()
        response = self.client.get(reverse('profile', kwargs={'pk': profile.pk}))
        self.assertContains(response, pet1.name)
        self.assertNotContains(response, pet2.name)
        self.assertListEqual(response.context['pets'], [pet1])
    def test_when_user_has_no_pets__Pets_Should_be_empty(self):
        user,profile = self.__create_valid_user_and_profile()
        response = self.client.get(reverse('profile', kwargs={'pk': profile.pk}))
        self.assertListEqual(response.context['pets'], [])

    def test_when_no_pets__Likes_and_photos_count__should_be_zero(self):
        pass
