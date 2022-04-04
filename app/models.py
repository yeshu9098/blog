from django.db import models
from django.urls import reverse
from account.models import CustomUser
from ckeditor.fields import RichTextField

# Create your models here.

class Contact(models.Model):
    user = models.ForeignKey(CustomUser,default=1, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    date = models.DateField()


    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=1000)

    def __str__(self):
        return self.title

class Post(models.Model):
    user = models.ForeignKey(CustomUser,default=1, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    #content = models.TextField(max_length=5000)
    content = RichTextField(blank=True, null=True)
    category = models.ForeignKey(Category, default="No category", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

