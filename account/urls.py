from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    path('login/', views.log_in, name='login'),
    path('register/', views.register, name='register'),
    path('edit_profile/<str:id>', views.edit_profile, name='edit_profile'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('confirmation_page/', views.active, name='active'),
    #path('edit_profile/<str:id>', views.edit_profile.as_view(), name='edit_profile'),
    path('password/', views.passwordsChangeView.as_view(template_name='account/password_change.html'), name='password'),
]