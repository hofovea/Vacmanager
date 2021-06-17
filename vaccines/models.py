from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from users.models import CustomUser


class LifePeriod(models.Model):
    class LifePeriods(models.IntegerChoices):
        BABY = 1, _('Baby under 18 months')
        CHILD = 2, _('Child from 2 to 16 years')
        ADULT = 3, _('Adult person over 16 years')

    life_period = models.IntegerField(
        choices=LifePeriods.choices,
        default=LifePeriods.BABY,
    )

    @property
    def get_life_period(self):
        if self.life_period == 1:
            return 'Немовля'
        elif self.life_period == 2:
            return 'Дитина'
        else:
            return 'Дорослий'


class AgePeriod(models.Model):
    class AgePeriods(models.IntegerChoices):
        ONE_DAY = 1, _('1 day of life')
        THREE_TO_FIVE_DAYS = 2, _('3 - 5 days of life')
        TWO_MONTHS = 3, _('2 months of life')
        FOUR_MONTHS = 4, _('4 months of life')
        SIX_MONTHS = 5, _('6 months of life')
        TWELVE_MONTHS = 6, _('12 months of life')
        EIGHTEEN_MONTHS = 7, _('18 months of life')
        SIX_YEARS = 8, _('6 years of life')
        FOURTEEN_YEARS = 9, _('14 years of life')
        SIXTEEN_YEARS = 10, _('16 years of life')
        ADULT = 11, _('17+ years of life')

    age_period = models.IntegerField(
        choices=AgePeriods.choices,
        default=AgePeriods.ONE_DAY,
    )
    life_period = models.ForeignKey(LifePeriod, on_delete=models.CASCADE, related_name='age_periods')

    @property
    def get_age_period(self):
        if self.age_period == 1:
            return '1 день'
        elif self.age_period == 2:
            return '2-5 днів'
        elif self.age_period == 3:
            return '2 місяці'
        elif self.age_period == 4:
            return '4 місяці'
        elif self.age_period == 5:
            return '6 місяців'
        elif self.age_period == 6:
            return '12 місяців'
        elif self.age_period == 7:
            return '18 місяців'
        elif self.age_period == 8:
            return '6 років'
        elif self.age_period == 9:
            return '14 років'
        elif self.age_period == 10:
            return '16 років'
        else:
            return 'Дорослий'


class Patient(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    age = models.IntegerField()
    birthday = models.DateField()
    address = models.OneToOneField("Address", on_delete=models.CASCADE)
    life_period = models.ForeignKey(LifePeriod, on_delete=models.CASCADE, related_name='patients')
    age_period = models.ForeignKey(AgePeriod, on_delete=models.CASCADE, related_name='patients')
    user = models.OneToOneField(CustomUser, null=True, blank=True, on_delete=models.CASCADE)

    @property
    def get_patient_data(self):
        return '{0} {1}, {2}'.format(self.name, self.surname, self.age)


class Queue(models.Model):
    date = models.DateField()
    is_active = models.BooleanField(default=True)
    patients = models.ManyToManyField(Patient, related_name='queues', null=True, blank=True)


class Vaccine(models.Model):
    name = models.TextField(max_length=50)
    patients = models.ManyToManyField(Patient, related_name='vaccines', through='VaccinationDate', null=True,
                                      blank=True)
    amount_of_doses = models.IntegerField()


class Address(models.Model):
    house = models.IntegerField()  # номер будинку
    street = models.CharField(max_length=100)  # вулиця
    town = models.CharField(max_length=100)  # населений пункт

    @property
    def full_address(self):
        return '{0}, {1} {2}'.format(self.town, self.street, self.house)


class VaccinationDate(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vaccination_dates')
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name='vaccination_dates')
    scheduled_date = models.DateField()
    actual_date = models.DateField(blank=True, null=True)
    number_of_dose = models.IntegerField()
