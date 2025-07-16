from django.contrib import admin
from .models import Employee,Department,Role,Contact


class MemberAdmin(admin.ModelAdmin):
    list_display=('name','department')
    search_fields=('name',)
    list_filter=('department',)
    


# Register your models here.
admin.site.register(Employee,MemberAdmin)
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(Contact)

