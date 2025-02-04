from django.contrib import admin
from .models import Task
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'due_date', 'priority', 'status', 'category', 'created_by', 'created_at']
    list_filter = ['priority', 'status', 'category', 'created_at']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
    list_per_page = 10
    ordering=['-created_at']
    
    def save_model(self, request, obj, form, change):
        
        if not obj.created_by and hasattr(request, 'user') and request.user.is_authenticated:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


# Register your models here.
