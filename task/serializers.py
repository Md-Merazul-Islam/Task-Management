from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Task
from datetime import datetime


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        # Automatically set 'created_by' to the logged-in user
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Automatically set 'created_by' to the logged-in user (in case it needs to be updated)
        validated_data['created_by'] = self.context['request'].user
        return super().update(instance, validated_data)

    def validate_media(self, media):
        if media:
            allowed_extensions = ['png', 'jpg', 'jpeg',
                                  'gif', 'mp4', 'avi', 'mov', 'mkv']
            max_size = 5*1024 * 1024
            if not media.name.lower().endswith(tuple(allowed_extensions)):
                raise serializers.ValidationError(
                    'File type should be one of the following: png, jpg, jpeg, gif, mp4, avi, mov, mkv')
            if media.size > max_size:
                raise serializers.ValidationError(
                    'File size should not exceed 5MB')
        return media

    def validate_due_date(self, value):
        """Ensure due date is not in the past"""
        if value < datetime.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value