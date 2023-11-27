from django.urls import path
from .views import SignIn, SignUp, EditUserData, EditPassword, LogOut, Profile

urlpatterns = [
    path('sign-in/', SignIn.as_view(), name='sign_in'),
    path('sign-up/', SignUp.as_view(), name='sign_up'),
    path('log-out/', LogOut.as_view(), name='log_out'),
    path('profile/', Profile.as_view(), name='profile'),
    path('edit-user-data/', EditUserData.as_view(), name='edit_user_data'),
    path('edit-password/', EditPassword.as_view(), name='edit_password'),
]
