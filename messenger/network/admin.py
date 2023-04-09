from django.contrib import admin

from .models import *

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'toWhom', 'fromWhom', 'photo', 'time_create', 'is_published']
    prepopulated_fields = {"slug": ("fromWhom",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Message, MessageAdmin)
admin.site.register(Category, CategoryAdmin)