from django import forms
from .models import Purchase

class PurchaseForm(forms.ModelForm):
   class Meta:
      model = Purchase
      fields = '__all__'

class Purchase_UploadExcelForm(forms.Form):
   excel_file = forms.FileField(label='Select an Excel file')