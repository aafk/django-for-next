from django.contrib.auth.models import User
from datetime import date
from django.forms import ModelForm
from .models import *

class AccountForm(ModelForm):
    def save(self, user_id):
        form = super().save(commit=False)
        form.date_created = date.today()
        form.user_created = User.objects.get(pk=user_id)
        form.save()
        return form
    class Meta:
        model = Account
        fields = ('__all__')
        exclude = ['user_created', 'date_created']

class CustomerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mobile2'].required = False
    def save(self, user_id):
        form = super().save(commit=False)
        form.person_role = True
        form.date_created = date.today()
        form.user_created = User.objects.get(pk=user_id)
        form.save()
        return form
    class Meta:
        model = Person
        fields = ('__all__')
        exclude = ['user_created', 'date_created']

class SupplierForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mobile2'].required = False
    def save(self, user_id):
        form = super().save(commit=False)
        form.person_role = False
        form.date_created = date.today()
        form.user_created = User.objects.get(pk=user_id)
        form.save()
        return form
    class Meta:
        model = Person
        fields = ('__all__')
        exclude = ['user_created', 'date_created']

class InventoryForm(ModelForm):
    def save(self, user_id):
        form = super().save(commit=False)
        form.date_created = date.today()
        form.user_created = User.objects.get(pk=user_id)
        form.save()
        return form
    class Meta:
        model = Inventory
        fields = ('__all__')
        exclude = ['user_created', 'date_created']

class DepreciationForm(ModelForm):
    def save(self, user_id):
        form = super().save(commit=False)
        form.date_created = date.today()
        form.user_created = User.objects.get(pk=user_id)
        form.save()
        return form
    class Meta:
        model = Depreciation
        fields = ('__all__')
        exclude = ['user_created', 'date_created']

class MeasureForm(ModelForm):
    def save(self, user_id):
        form = super().save(commit=False)
        form.date_created = date.today()
        form.user_created = User.objects.get(pk=user_id)
        form.save()
        return form
    class Meta:
        model = Measure
        fields = ('__all__')
        exclude = ['user_created', 'date_created']