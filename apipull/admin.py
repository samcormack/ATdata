from django.contrib import admin
from .models import RTentry, CallRecord, Route, Stop

# Register your models here.
admin.site.register(RTentry)
admin.site.register(CallRecord)
admin.site.register(Route)
admin.site.register(Stop)
