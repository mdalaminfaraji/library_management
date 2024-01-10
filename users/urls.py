from django.urls import path
from .import views
urlpatterns = [
    path('register/', views.Register, name="register"),
    path('login/', views.SignUP, name="login"),
    path('profile/', views.profile, name="profile"),
    path('update_profile/', views.edit_profile, name="edit_profile"),
    path('logout/', views.user_logout, name="logout"),
    path('deposit/', views.deposit_money, name='deposit_money'),
]
