from django.contrib import admin
from .models import *

from image_cropping import ImageCroppingMixin
from django.contrib.auth.models import Group

# Register your models here.
#admin.site.register(Doctor)

#admin.site.register(SomeImage)

admin.site.site_header = 'Cancer App Admin Site'
admin.site.site_title = 'Cancer App Management'

class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass

#admin.site.register(Patient, MyModelAdmin)
admin.site.unregister(Group)

@admin.register(Doctor)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("username",'email',"fname", "lname")
    list_filter = ("created",)
    #prepopulated_fields = {'slug':('patient_id')}

@admin.register(Patient)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('fname','lname','doctor',"patient_id")
    list_filter = ("created",)

