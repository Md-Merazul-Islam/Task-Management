from rest_framework import status
from rest_framework.response import Response
from django.db import models
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import serializers, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Task
from .serializers import TaskSerializer

User = get_user_model()

# Max file size (5MB)
MAX_SIZE = 5 * 1024 * 1024


def success_response(message, data=None, status_code=200):
    response = {
        "success": True,
        "statusCode": status_code,
        "message": message,
    }
    if data is not None:
        response["data"] = data
    return Response(response, status=status_code)


def error_response(message, error_details=None, status_code=400):
    response = {
        "success": False,
        "message": message,
    }
    if error_details is not None:
        response["errorDetails"] = error_details
    return Response(response, status=status_code)


class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'category', 'tags']
    ordering_fields = ['priority', 'status', 'due_date']
    ordering = ['created_at']

    def get_queryset(self):
        """Superusers see all tasks; others see only their own."""
        if self.request.user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        """Validate file size and send a due date reminder after creating a task."""
        media_file = self.request.FILES.get('media')
        if media_file and media_file.size > MAX_SIZE:
            return error_response('File size should not exceed 5MB')

        task = serializer.save(created_by=self.request.user)
        self.send_due_date_reminder(task)

    def perform_update(self, serializer):
        task = serializer.instance
        file = self.request.FILES.get('media')
        if file and file.size > MAX_SIZE:
            return error_response('File size should not exceed 5MB')
        prev_status = task.status
        # serializer.save()

        if self.request.user.is_superuser:
            serializer.save()
        elif task.created_by == self.request.user:
            serializer.save(status='in_progress')
        else:
            raise ValidationError(
                'You do not have permission to update this task')

        if prev_status != 'completed' and serializer.instance.status == 'completed':
            self.send_task_completion_email(serializer.instance)
        return success_response("Task updated successfully", {"task": TaskSerializer(serializer.instance).data})
    def perform_destroy(self, instance):
        """Only allow task deletion if the user is the creator or a superuser."""
        if self.request.user.is_superuser or instance.created_by == self.request.user:
            instance.delete()
            return success_response('Task deleted successfully')
        return error_response('You do not have permission to delete this task')

    def send_due_date_reminder(self, task):
        """Send an email reminder about the due date."""
        subject = f"Reminder: Task '{task.title}' is due on {task.due_date}"
        message = f"Dear {task.created_by.username},\n\nYour task '{task.title}' is due on {task.due_date}. Please ensure to complete it on time.\n\nThank you!"
        recipient_list = [task.created_by.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)

    def send_task_completion_email(self, task):
        """Send an email when the task is marked as completed."""
        subject = f"Task Completed: {task.title}"
        message = f"Dear {task.created_by.username},\n\nCongratulations! Your task '{task.title}' has been marked as completed.\n\nThank you!"
        recipient_list = [task.created_by.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)