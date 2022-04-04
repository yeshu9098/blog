from django.contrib import admin
from app.models import Category, Contact, Post
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','category','date','user')
    search_fields = ('title',)
    list_filter = ('category',)
    list_per_page = 20

class ContactAdmin(admin.ModelAdmin):
    list_display = ('user','message','date')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Contact, ContactAdmin)