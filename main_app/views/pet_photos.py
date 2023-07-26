import os
import shutil

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic as views


from ..forms import CreatePetPhotoForm, EditPetPhotoForm
from ..models import PetPhoto, Pet


class ShowPetPhotoDetail(LoginRequiredMixin,views.DetailView):
    model = PetPhoto
    template_name = 'photo_details.html'
    context_object_name = 'pet_photo'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] =self.object.user == self.request.user
        return context

#Written in FBV
#-------------------------------------------------
# def show_pet_photo_details(request,pk):
#     pet = PetPhoto.objects.get(id=pk)
#     context={
#         'pet_photo':pet,
#     }
#     return render(request,'photo_details.html',context)


def like_pet(request,pk):
    pet_photo = PetPhoto.objects.prefetch_related('tagged_pets').get(pk=pk)
    pet_photo.description="Mishka"
    pet_photo.likes+=1
    pet_photo.save()
    return redirect('pet_photo_details',pk)


class CreatePetPhotoView(LoginRequiredMixin,views.CreateView):

    template_name = 'photo_create.html'
    form_class = CreatePetPhotoForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user_pets = Pet.objects.filter(user=self.request.user)
        form.fields['tagged_pets'].queryset = user_pets

        #form.fields['tagged_pets'].choices = [(p.id,p.name) for p in user_pets]
        return form

#Written in FBV
#-------------------------------------------------
# def create_pet_photo(request):
#     if request.method == "POST":
#         pet_photo_form = CreatePetPhotoForm(request.POST,request.FILES)
#         if pet_photo_form.is_valid():
#             pet_photo_form.save()
#             return redirect('dashboard')
#     else:
#         pet_photo_form = CreatePetPhotoForm()
#
#     context={
#         'pet_photo_form':pet_photo_form,
#     }
#
#     return render(request,'photo_create.html',context)

class EditPetPhotoView(views.UpdateView):
    model = PetPhoto
    template_name = 'photo_edit.html'
    form_class = EditPetPhotoForm
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pet'] = self.object
        return context
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user_pets = Pet.objects.filter(user=self.request.user)
        form.fields['tagged_pets'].queryset = user_pets
        return form
    def form_valid(self, form):
        photo = form.instance
        current_photo=PetPhoto.objects.get(pk=photo.pk)
        if photo.photo:
            photo_path = current_photo.photo.path
            if os.path.exists(photo_path):
                os.remove(photo_path)
        uploaded_photo = self.request.FILES.get('photo')
        if uploaded_photo:
            # Save the uploaded photo file
            photo.photo = uploaded_photo
        return super().form_valid(form)


def edit_pet_photo(request,pk):
    pet_photo = PetPhoto.objects.get(pk=pk)
    if request.method == "POST":
        pet_photo_form = EditPetPhotoForm(request.POST, instance=pet_photo)
        if pet_photo_form.is_valid():
            pet_photo_form.save()
            return redirect('dashboard')
    else:
        pet_photo_form = EditPetPhotoForm(instance=pet_photo)

    context = {
        'pet_photo_form': pet_photo_form,
        'pet':pet_photo,
    }
    return render(request,'photo_edit.html',context)