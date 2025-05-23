from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Define an inline admin descriptor for Profile model
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'
    fields = ('voter_name', 'house', 'voter_class')

# Define a new User admin that includes the Profile
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    
    # Define methods to access Profile fields with sorting support
    def voter_name(self, obj):
        return obj.profile.voter_name if hasattr(obj, 'profile') else 'N/A'
    voter_name.short_description = 'Voter Name'
    voter_name.admin_order_field = 'profile__voter_name'
    
    def voter_class(self, obj):
        return obj.profile.voter_class if hasattr(obj, 'profile') else 'N/A'
    voter_class.short_description = 'Class'
    voter_class.admin_order_field = 'profile__voter_class'
    
    def house(self, obj):
        return obj.profile.house if hasattr(obj, 'profile') else 'N/A'
    house.short_description = 'House'
    house.admin_order_field = 'profile__house'
    
    # Set the fields to display in the admin list view
    list_display = ('voter_name', 'username', 'voter_class', 'house')
    
    # Optimize database queries by fetching the related Profile
    list_select_related = ('profile',)
    
    # Enable searching by voter_name and username
    search_fields = ['profile__voter_name', 'username']
    
    # Optional: Add filters for house and voter_class
    list_filter = ('profile__house', 'profile__voter_class')

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)