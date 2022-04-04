from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path('', views.index, name='index'),
    path('api', views.api, name='api'),
    path('addpost', views.addpost, name='addpost'),
    path('post/<str:id>', views.post, name='post'),
    path('post/<str:id>/delete', views.delete, name='delete'),
    path('post/<str:id>/update', views.update, name='update'),
    path('category/<str:title>', views.category, name='category'),
    path('profile/<str:id>', views.profile, name='profile'),
    path('contact/', views.contact, name='contact'),
    path('logout/', views.log_out, name='logout'),
]