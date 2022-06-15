from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin




UserAdmin.fieldsets += (
    (None, {'fields':('is_author', 'image', 'info', 'job', 'linkedin', 'twitter', 'instagram', 'github', 'telegram', 'website')}),
)
UserAdmin.list_display += ('is_author',)
admin.site.register(User, UserAdmin)
