from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(LifePeriod)
admin.site.register(AgePeriod)
admin.site.register(Patient)
admin.site.register(Address)
admin.site.register(VaccinationDate)
admin.site.register(Vaccine)
admin.site.register(Queue)
