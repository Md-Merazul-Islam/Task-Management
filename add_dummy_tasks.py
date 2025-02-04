from django.core.management.base import BaseCommand
from task.models import Task
from django.contrib.auth import get_user_model
from datetime import date
import random

User = get_user_model()

class Command(BaseCommand):
    help = "Adds dummy task data to the database"

    def handle(self, *args, **kwargs):
        user = User.objects.first()  

        tasks = [
            Task(
                title=f"Task {i}",
                description=f"Description for task {i}",
                due_date=date(2024, random.randint(1, 12), random.randint(1, 28)),
                priority=random.choice(['low', 'medium', 'high']),
                status=random.choice(['not_started', 'in_progress', 'completed']),
                category=random.choice(["Work", "Personal", "Study"]),
                tags="tag1, tag2",
                created_by=user
            )
            for i in range(10)  
        ]

        Task.objects.bulk_create(tasks)
        self.stdout.write(self.style.SUCCESS("Successfully added dummy tasks!"))
