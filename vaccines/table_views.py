from django_filters.views import FilterView
from django_tables2 import SingleTableMixin, SingleTableView

from .models import Patient, VaccinationDate
from .table_filters import PatientFilter, VaccinationFilter
from .tables import PatientTable, VaccinationTable


# class PatientListView(SingleTableView):
#     model = Patient
#     table_class = PatientTable
#     template_name = 'vaccination/vaccination_results.html'
class PatientListView(SingleTableMixin, FilterView):
    table_class = PatientTable
    model = Patient
    template_name = "vaccination/vaccination_results.html"
    filterset_class = PatientFilter


class VaccinationListView(SingleTableMixin, FilterView):
    model = VaccinationDate
    table_class = VaccinationTable
    template_name = 'vaccination/vaccination_results.html'
    filterset_class = VaccinationFilter
