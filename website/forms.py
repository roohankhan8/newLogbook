from django import forms
from .models import * 

class RecordOfInventionForm(forms.ModelForm):
  class Meta:
    model = RecordOfInvention
    fields = '__all__'  # Include all fields
    exclude = ['userId', 'teamId', ...]

class StatementOfOriginalityForm(forms.ModelForm):
  class Meta:
    model = StatementOfOriginality
    fields = "__all__"
    exclude = ['userId', 'teamId', ...]

class StepOneForm(forms.ModelForm):
  model = StepOne
  fields = "__all__"
  exclude = ['userId', 'teamId', ...]