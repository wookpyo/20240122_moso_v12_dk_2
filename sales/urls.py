from django.urls import path
from .views import sales_main, sales_UploadExcelForm

app_name = 'sales'

urlpatterns = [
    path('', sales_main, name='sales_main'),
    path('sales_UploadExcelForm/', sales_UploadExcelForm, name='sales_UploadExcelForm'),
    # path('list/', sales_list, name='sales_list'),
    # path('add/', add_sales, name='add_sales'),
    # path('upload/', sales_upload_excel, name='sales_upload_excel'),
    # path('sale/list/', SaleListView.as_view(), name='sale-list'),
   
]