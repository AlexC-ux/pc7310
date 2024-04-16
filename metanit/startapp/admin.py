from django.contrib import admin
from startapp.models import Contacts, TestTexts

# Register your models here.
class ContactsAdmin(admin.ModelAdmin):
    list_display = ["name", "phone","surname","post"]
    search_fields = ["name","phone","surname","post"]

class ContentAdmin(admin.ModelAdmin):
    list_display = ["page_name","html_content", ]
    search_fields = ["html_content", "page_name",]

admin.site.register(Contacts, ContactsAdmin)
admin.site.register(TestTexts, ContentAdmin)