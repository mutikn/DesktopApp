from django.contrib import admin
from application.models import User, Comment

admin.site.register(User)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display =('comment', 'creator')
    fields = ('comment', 'creator', 'created',)
    readonly_fields = ('created',)
