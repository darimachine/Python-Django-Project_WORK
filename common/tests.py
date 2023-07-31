from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from common.validators import ValidateFileMaxSizeInMB
from main_app.models import Pet, PetPhoto

UserModel = get_user_model()
class MaxFileSizeInMBValidatorTest(TestCase):
    def test_when_file_is_bigger__Expect_to_raise_error(self):
        user = UserModel.objects.create_user(
            username='test',
            password='test213',
        )
        pet = Pet.objects.create(
            name='Kotka',
            type='Cat',
            user=user,
        )

        # Create a file with size larger than 5 MB (you can adjust the size as needed)
        large_file = SimpleUploadedFile("large_image.png", b"0" * (6 * 1024 * 1024))  # 6 MB file

        # Attempt to create a PetPhoto with the large file
        pet_photo = PetPhoto.objects.create(
            photo=large_file,
            user=user,
        )
        pet_photo.tagged_pets.add(pet)
        pet_photo.save()

        # Create the validator with max_size=5 MB
        validator = ValidateFileMaxSizeInMB(5)

        # Check that the validator raises a ValidationError when applied to the PetPhoto instance
        with self.assertRaises(ValidationError) as context:
            validator(pet_photo.photo)
            self.assertEqual(context.exception.message, "Max file size is 5MB")

    def test_when_file_size_is_valid___Expect_to_not_raise_error(self):
        pass