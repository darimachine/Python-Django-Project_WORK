from django.urls import path
from django.views.generic import RedirectView

from accounts import views
from accounts.views import *

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login user'),
    #profile

    path('<int:pk>',ShowProfileView.as_view(),name='profile'),
    path('register/',UserRegisterView.as_view(),name='create_profile'),
    path('edit/<int:pk>', EditUserProfileView.as_view(), name='edit_profile'),
    path('edit-password/',ChangePasswordView.as_view(),name='change password'),
    path('password_change_done/',RedirectView.as_view(url=reverse_lazy('dashboard')),name='password_change_done'),
    path('logout/', MyLogOutView.as_view(), name='logout user'),
    #path('profile/delete/', delete_profile, name='delete_profile'),
]