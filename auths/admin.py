from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

# Custom User Admin class
class CustomUserAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']
    
    # Fields to be used as filters in the sidebar
    list_filter = ['is_staff', 'is_active', 'date_joined']
    
    # Search fields that allow searching by username or email
    search_fields = ['username', 'email']
    
    # Fields to be editable in the list view
    list_editable = ['is_active']
    
    # Fields to display in the detail view
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Make sure password is not displayed in the admin
    readonly_fields = ['password']
    
    # Add extra fields for adding or changing a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active')}
        ),
    )
    
    # Custom save method to handle user password and other extra logic
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new user
            obj.set_password(obj.password)  # Ensure password is hashed
        super().save_model(request, obj, form, change)

# Register the User model with the custom admin class
admin.site.register(User, CustomUserAdmin)
