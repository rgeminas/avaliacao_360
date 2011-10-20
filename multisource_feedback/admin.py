from models import *
#from gp_utils.common.models import Board, Member
from django.contrib import admin


class MemberInline(admin.StackedInline):
    model = Member
    extra = 3

class BoardAdmin(admin.ModelAdmin):
    inlines = [MemberInline]

class FeedbackSetAdmin(admin.ModelAdmin):
    pass

admin.site.register(Member)
admin.site.register(FeedbackSet)
admin.site.register(FeedbackMember)
admin.site.register(Board, BoardAdmin)
