from django.contrib import admin
from .models import School, Staff


class StaffInline(admin.TabularInline):
    model = Staff
    extra = 0


class SchoolAdmin(admin.ModelAdmin):
    inlines = [StaffInline, ]


admin.site.register(School, SchoolAdmin)
