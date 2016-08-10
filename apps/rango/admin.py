from django.contrib import admin

# Register your models here.
from .models import Category, Page
from .models import UserProfile


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


# Register Model, Must First register
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page)

admin.site.register(UserProfile)
