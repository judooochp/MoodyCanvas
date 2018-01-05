from django.contrib import admin
from .models import Customer, Plate, Verif, Profile, Meas

# Register your models here.
admin.site.register(Customer)
admin.site.register(Plate)
admin.site.register(Verif)
admin.site.register(Profile)
admin.site.register(Meas)
