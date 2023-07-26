from django.contrib.auth import forms as auth_forms, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views
from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView
from accounts.forms import *
from accounts.models import Profile
from common.helpers import get_profile
from common.view_mixins import RedirectToDashboard
from main_app.models import Pet


#Written with FBV
#--------------------------------------
# def create_profile(request):
#     if request.method == 'POST':
#         profile_form=CreateProfileForm(request.POST, request.FILES)
#         if profile_form.is_valid():
#             profile_form.save()
#             return redirect('dashboard')
#     else:
#         profile_form = CreateProfileForm()
#
#     context={
#         'profile_form':profile_form,
#     }
#     return render(request,'profile_create.html',context)
#Written with CBV
#--------------------------------------
class UserRegisterView(RedirectToDashboard,views.CreateView):
    template_name = 'accounts/profile_create.html'
    form_class = CreateProfileForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result

class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login_user.html'
    success_url = reverse_lazy('dashboard')

    # def form_valid(self, form):
    #     result = super().form_valid(form)
    #     login(self.request, self.object)
    #     return result
#Written with FBV
#--------------------------------------
# def edit_profile(request):
#     profile = get_profile()
#     if request.method == 'POST':
#         profile_form= EditProfileForm(request.POST, instance=profile)
#         if profile_form.is_valid():
#             profile_form.save()
#             return redirect('profile')
#     else:
#         profile_form = EditProfileForm(instance=profile)
#
#     context={
#         'profile_form':profile_form,
#     }
#     return render(request,'profile_edit.html',context)

#Written with CBV
#--------------------------------------
class EditUserProfileView(views.UpdateView):
    template_name = 'accounts/profile_edit.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('dashboard')
    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


class ChangePasswordView(auth_views.PasswordChangeView):
    template_name = 'accounts/change_password.html'

# Written with FBV
#--------------------------------------------------------
# def show_profile(request):
#     profile = get_profile()
#     pets = Pet.objects.filter(user_profile=profile)
#     pet_photos = PetPhoto.objects.filter(tagged_pets__in=pets).distinct()
#     total_likes_count = sum(pp.likes for pp in pet_photos)
#     total_pet_photos_count = len(pet_photos)
#     #------- НЕ ОПТИМИЗИРАН ВАРИАНТ
#         # total_likes_count = sum(photo.likes for photo in PetPhoto.objects.filter(tagged_pets__user_profile=profile).distinct())
#         # total_pet_photos_count =len(PetPhoto.objects.filter(tagged_pets__user_profile=profile).distinct())
#     context = {
#         'profile':profile,
#         'total_likes_count': total_likes_count,
#         'total_images_count':total_pet_photos_count,
#         'pets':pets,
#     }
#     return render(request,'profile_details.html',context)
#Written with CBV
#--------------------------------------------------------
class ShowProfileView(views.DetailView):
    model = Profile
    template_name = 'profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pets = list(Pet.objects.filter(user_id=self.object.user_id))
        pet_photos = PetPhoto.objects.filter(tagged_pets__in=pets).distinct()
        total_likes_count = sum(pp.likes for pp in pet_photos)
        total_pet_photos_count = len(pet_photos)
        context['total_likes_count'] = total_likes_count
        context['total_images_count'] = total_pet_photos_count
        context['pets'] = pets
        context['is_owner'] = self.object.user_id == self.request.user.id
        return context

class MyLogOutView(LogoutView):
    next_page = reverse_lazy('index')



def delete_profile(request):
    profile = get_profile()
    if request.method == 'POST':
        profile_form = DeleteProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('index')
    else:
        profile_form = DeleteProfileForm(instance=profile)

    context = {
        'profile_form': profile_form,
    }
    return render(request, 'accounts/profile_delete.html', context)


