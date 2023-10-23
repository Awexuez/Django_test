from django.urls import path
from users.views import login, profile, logout, UserRegistrationView

app_name = "users"

urlpatterns = [
    path("login/", login, name="login"),
    # path('registration/', registration, name = 'registration'),
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    # path('profile/<int:pk>/', UserProfileView.as_view(), name = 'profile'),
    path("profile/", profile, name="profile"),
    path("logout/", logout, name="logout"),
]
