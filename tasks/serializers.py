# tasks/serializers.py
from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # expose all fields to API
        fields = "__all__"

        # these are auto-generated or managed by the system
        read_only_fields = [
            "id",  # primary key, auto-generated
            "slug",  # auto-generated slug from title
            "created_at",  # timestamp set automatically
            "updated_at",  # timestamp set automatically
            "transcript",  # will be filled by AI after audio processing
        ]
