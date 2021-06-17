from django_tables2 import tables

from vaccines.models import Patient, VaccinationDate


class PatientTable(tables.Table):
    address = tables.columns.Column(accessor='address.full_address', order_by='address.street')
    life_period = tables.columns.Column(accessor='life_period.get_life_period', order_by='life_period.life_period')
    age_period = tables.columns.Column(accessor='age_period.get_age_period', order_by='age_period.age_period')

    class Meta:
        model = Patient
        attrs = {"class": "table table-hover"}
        # template_name = "django_tables2/bootstrap.html"


class VaccinationTable(tables.Table):
    patient = tables.columns.Column(accessor='patient.get_patient_data', order_by='patient.age')
    vaccine = tables.columns.Column(accessor='vaccine.name')
    amount_of_doses = tables.columns.Column(accessor='vaccine.amount_of_doses')

    class Meta:
        model = VaccinationDate
        attrs = {"class": "table table-hover"}
        # template_name = "django_tables2/bootstrap.html"
