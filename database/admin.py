from django.contrib import admin
from database.models import *
from import_export.admin import ImportExportModelAdmin

class UserAdmin(admin.ModelAdmin):
    list_display=('username','user_type','password')

# Register your models here.
admin.site.register(CustomUser,UserAdmin)
admin.site.register(Contact,ImportExportModelAdmin)
