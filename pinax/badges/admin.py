from django.contrib import admin

from .models import BadgeAward


class BadgeAwardAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]


admin.site.register(BadgeAward, BadgeAwardAdmin)
