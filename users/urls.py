from django.urls import path
from users.views import ToggleFollowView

from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('refresh/', TokenRefreshView.as_view(), name="token_refresh"),

    path('<int:user_id>/follow-toggle/', ToggleFollowView.as_view(), name="toggle_follow"),
]
