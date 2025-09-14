# tasks/admin.py
from django.contrib import admin
from .models import Task


# tasks/admin.py
from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "time", "type", "slug")
    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
    )  # slug is readonly
