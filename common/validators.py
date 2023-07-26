from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
def only_letters_validator(value):
    for ch in value:
        if not ch.isalpha():
            raise ValidationError(
                _('%(value) is not only letter'),
            params={'value': value},
                                  )

@deconstructible
class ValidateFileMaxSizeInMB:
    def __init__(self,max_size):
        self.max_size = max_size
    def __call__(self, value, *args, **kwargs):
        filesize = value.file.size
        if filesize > self.max_size * 1024 * 1024:
            raise ValidationError(f"Max file size is {self.max_size}MB")

def atleastOnePet(value):
    if value.count<1:
        raise ValidationError('You need to have atleast 1 tagged pets')
