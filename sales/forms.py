from django import forms
from .models import Sales

class SalesForm(forms.ModelForm):
   class Meta:
      model = Sales
      fields = '__all__'

class Sales_UploadExcelForm(forms.Form):
   excel_file = forms.FileField(label='Select an Excel file')