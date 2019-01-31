from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Projects)
admin.site.register(Comment)
admin.site.register(Rate)
admin.site.register(Categories)
admin.site.register(Supplier)
admin.site.register(ReportComment)
admin.site.register(ReportProject)
admin.site.register(ImageProject)

