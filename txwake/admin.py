from django.contrib import admin
from .models import BoatPull, BoatPullSignup, EmailSubscription
import csv
from django.http import HttpResponse

def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="emails.csv"'
    writer = csv.writer(response)
    writer.writerow(['Email', 'Date Subscribed'])

    for subscription in queryset:
        writer.writerow([subscription.email, subscription.date_subscribed])

    return response

export_to_csv.short_description = "Export Selected to CSV"
@admin.register(EmailSubscription)
class EmailSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscribed')
    actions = [export_to_csv]



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

@admin.register(BoatPullSignup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ('user', 'boat_pull', 'signup_time')
    list_filter = ('boat_pull', 'user')