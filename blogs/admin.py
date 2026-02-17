from django.contrib import admin
from .models import category, Blog

@admin.register(category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'created_at')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author', 'status', 'is_featured', 'created_at')
    list_filter = ('status', 'is_featured', 'category')
    prepopulated_fields = {'slug': ('title',)}
