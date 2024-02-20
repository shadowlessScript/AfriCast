from django.contrib import admin
from .models import Repository

# Register your models here.
@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ("website", "title")