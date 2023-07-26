from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic as views
from django.shortcuts import render, redirect

from ..forms import CreatePetForm, EditPetForm, DeletePetForm

from ..models import PetPhoto, Pet

UserModel=get_user_model()

class CreatePetView(views.CreateView):
    template_name = 'pet_create.html'
    form_class = CreatePetForm
    success_url = reverse_lazy('dashboard')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EditPetView(views.UpdateView):
    template_name = "pet_edit.html"
    form_class = EditPetForm

class DeletePetView(views.DeleteView):
    template_name = "pet_delete.html"
    success_url = reverse_lazy('dashboard')
    form_class = DeletePetForm

# def create_pet(request):
#     if request.method == "POST":
#         pet_form = CreatePetForm(request.POST,instance=Pet(user_profile=get_profile()))
#         if pet_form.is_valid():
#             pet_form.save()
#             return redirect('profile')
#     else:
#         pet_form = CreatePetForm()
#
#     context={
#         'pet_form':pet_form,
#     }
#     return render(request,'pet_create.html',context)
#
# def edit_pet(request,pk):
#     pet = Pet.objects.get(pk=pk)
#     if request.method == "POST":
#         pet_form = CreatePetForm(request.POST, instance=pet)
#         if pet_form.is_valid():
#             pet_form.save()
#             return redirect('profile')
#     else:
#         pet_form = CreatePetForm(instance=pet)
#
#     context = {
#         'pet_form': pet_form,
#         'pet':pet,
#     }
#     return render(request, 'pet_edit.html', context)
#
#
# def delete_pet(request,pk):
#     pet = Pet.objects.get(pk=pk)
#     if request.method == "POST":
#         pet_form = DeletePetForm(request.POST, instance=pet)
#         if pet_form.is_valid():
#             pet_form.save()
#             return redirect('profile')
#     else:
#         pet_form = DeletePetForm(instance=pet)
#
#     context = {
#         'pet_form': pet_form,
#         'pet': pet,
#     }
#
#     return render(request,'pet_delete.html',context)