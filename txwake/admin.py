from django.contrib import admin
from .models import BoatPull, Signup

@admin.register(BoatPull)
class BoatPullAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'max_capacity', 'available_spots', 'is_active')
    list_filter = ('date', 'is_active')
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    make_active.short_description = "Make selected boat pulls active"
    make_inactive.short_description = "Make selected boat pulls inactive"

@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ('user', 'boat_pull', 'signup_time')
    list_filter = ('boat_pull', 'user')