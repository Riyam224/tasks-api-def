# tasks/admin.py
from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # list_display = ("id", "title", "type", "date", "time", "created_at")
    search_fields = ("title", "content", "transcript")
    list_filter = ("type", "date", "created_at")
    ordering = ("-created_at",)
