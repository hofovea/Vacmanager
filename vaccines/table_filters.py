import django_filters
from django.forms import CheckboxSelectMultiple

from vaccines.models import Patient, VaccinationDate, Vaccine


class PatientFilter(django_filters.FilterSet):
    class Meta:
        model = Patient
        fields = ['name', 'surname', 'age', 'birthday', 'address__house', 'address__street', 'address__town',
                  'age_period', 'life_period']


class VaccinationFilter(django_filters.FilterSet):
    patient_filter = django_filters.AllValuesFilter('patient')

    class Meta:
        model = VaccinationDate
        fields = ['actual_date', 'scheduled_date', 'number_of_dose', 'vaccine__name',
                  'vaccine__amount_of_doses']
