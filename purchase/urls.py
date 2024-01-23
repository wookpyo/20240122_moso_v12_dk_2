from django.urls import path
from .views import purchase_main, purchase_UploadExcelForm

app_name = 'purchase'

urlpatterns = [
    path('', purchase_main, name='purchase_main'),
    path('purchase_UploadExcelForm/', purchase_UploadExcelForm, name='purchase_UploadExcelForm'),
    # path('list/', sales_list, name='sales_list'),
    # path('add/', add_sales, name='add_sales'),
    # path('upload/', sales_upload_excel, name='sales_upload_excel'),
    # path('sale/list/', SaleListView.as_view(), name='sale-list'),
   
]