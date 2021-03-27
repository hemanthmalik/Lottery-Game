from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models as main_models
from django.contrib.auth import get_user_model

User = get_user_model()

class MyUserAdmin(UserAdmin):
    model = User
    list_display = ['id', 'name', 'phone', 'email', 'balance', 'is_active']  # Contain only fields in your `custom-user-model`
    list_filter = ()  # Contain only fields in your `custom-user-model` intended for filtering. Do not include `groups`since you do not have it
    search_fields = ()  # Contain only fields in your `custom-user-model` intended for searching
    ordering = ()  # Contain only fields in your `custom-user-model` intended to ordering
    filter_horizontal = () # Leave it empty. You have neither `groups` or `user_permissions`
    fieldsets = (
            (None, {'fields': ('phone', 'password')}),
    )
    add_fieldsets = (
            (None, {'fields': ('name', 'phone', 'email', 'password1', 'password2')}),
    )

# Register your models here.
admin.site.register(User, MyUserAdmin)
@admin.register(main_models.AddedAmount)
class AddedAmountAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

@admin.register(main_models.Bet)
class BetAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

@admin.register(main_models.Win)
class WinnsAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]