from django.urls import path
from .views import EmployeeListView, SignupView, CurrentUserView, GetUserByEmailView, GetUserByIdView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', SignupView.as_view(), name='register_view'),
    path('login/', TokenObtainPairView.as_view(), name='login_view'),
    path('refresh_token/', TokenRefreshView.as_view(), name='refresh_token_view'),
    path('user/', CurrentUserView.as_view(), name='current_user_view'),
    path('employees/', EmployeeListView.as_view(), name='employees_list'),
    path('user/by_email/', GetUserByEmailView.as_view(), name='get-user-by-email'),
    path('user/<int:user_id>/', GetUserByIdView.as_view(), name='get_user_by_id')
]
