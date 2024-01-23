from django.shortcuts import render, redirect
from .forms import Sales_UploadExcelForm
import pandas as pd
from decimal import Decimal
import math
from .models import Sales

from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.express as px
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.db.models.functions import TruncYear

# Create your views here.
def sales_main(request):
   sales_data = Sales.objects.all()
   sales_dates = [item.written_date for item in sales_data]
   sales_values = [item.total_amount for item in sales_data]

   # # Purchase 데이터 가져오기
   # purchase_data = Purchase.objects.all()
   # purchase_dates = [item.written_date for item in purchase_data]
   # purchase_values = [item.total_amount for item in purchase_data]


   # Sales 데이터 월별 합산
   sales_data_monthly = Sales.objects.annotate(month=TruncMonth('written_date')).values('month').annotate(total_amount=Sum('total_amount'))

   # # Purchase 데이터 월별 합산
   # purchase_data_monthly = Purchase.objects.annotate(month=TruncMonth('issue_date')).values('month').annotate(total_amount=Sum('total_amount'))
   fig = make_subplots(rows=1, cols=1, subplot_titles=['Sales and Purchase Data'])
   fig.add_trace(go.Scatter(x=sales_dates, y=sales_values, mode='lines', name='Sales'))
   ###################
   # 년단위 합산으로 변경
   sales_data_yearly = Sales.objects.annotate(year=TruncYear('written_date')).values('year').annotate(total_amount=Sum('total_amount'))
   # 년단위 그래프로 변경
   fig3 = make_subplots(rows=1, cols=1, subplot_titles=['Sales and Purchase Yearly Data'])
   fig3.add_trace(go.Bar(
      x=[item['year'] for item in sales_data_yearly],  # x축을 year로 변경
      y=[item['total_amount'] for item in sales_data_yearly],
      name='Sales',
      marker_color='blue'
   ))
   fig3.update_layout(
      title_text='Sales and Purchase Yearly Data',  # 제목을 Yearly Data로 수정
      xaxis_title='Year',  # x축 라벨을 Year로 수정
      yaxis_title='Total Amount',
      barmode='group'
   )
   fig3.update_yaxes(tickformat=',')
#    fig3 = make_subplots(rows=1, cols=1, subplot_titles=['Sales and Purchase Data'])
#    fig3.add_trace(go.Scatter(x=sales_dates, y=sales_values, mode='lines+markers', name='Sales'))
   graph3 = fig3.to_html(full_html=False)
   ################
   # fig.add_trace(go.Scatter(x=purchase_dates, y=purchase_values, mode='lines', name='Purchase'))

   # fig.update_layout(title_text='Sales and Purchase Data', xaxis_title='Date', yaxis_title='Amount')
   # graph1 = fig.to_html(full_html=False)
   fig.update_yaxes(tickformat=',')
   print("Sales Data:")
   for item in sales_data_monthly:
      print(item)
   graph1 = fig.to_html(full_html=False)
      ###################
   fig2 = make_subplots(rows=1, cols=1, subplot_titles=['Sales and Purchase Monthly Data'])
   fig2.add_trace(go.Bar(
      x=[item['month'] for item in sales_data_monthly],
      y=[item['total_amount'] for item in sales_data_monthly],
      name='Sales',
      marker_color='blue'
   ))
      
   # fig2.add_trace(go.Bar(
   #     x=[item['month'] for item in purchase_data_monthly],
   #     y=[item['total_amount'] for item in purchase_data_monthly],
   #     name='Purchase',
   #     marker_color='orange'
   # ))

   fig2.update_layout(
         title_text='Sales and Purchase Monthly Data',
         xaxis_title='Month',
         yaxis_title='Total Amount',
         barmode='group'
   )

   # Y 축의 형식을 설정 (예: 1,000단위 콤마 표시)
   fig2.update_yaxes(tickformat=',')
   print("Sales Data:")
   for item in sales_data_monthly:
         print(item)
   graph2 = fig2.to_html(full_html=False)

   context = {
         'graph1': graph1,
         'graph2': graph2,
         'graph3': graph3,
   }

   return render(request, 'sales/sales_main.html', context)

def sales_UploadExcelForm(request):
   if request.method == 'POST':
      form = Sales_UploadExcelForm(request.POST, request.FILES)
      if form.is_valid():
         excel_file = request.FILES['excel_file']
      if excel_file.name.endswith('.csv'):
         df = pd.read_csv(excel_file)
      elif excel_file.name.endswith('.xlsx'):
         df = pd.read_excel(excel_file, engine='openpyxl', skiprows=1)
      else:
         return render(request, 'sales_invalid_file_format.html')
            
      column_mapping = {
         1: 'written_date',
         2: 'approval_number',
         3: 'issue_date',
         4: 'transmission_date',
         5: 'supplier_registration_number',
         6: 'supplier_branch_number',
         7: 'supplier_business_name',
         8: 'supplier_representative_name',
         9: 'supplier_address',
         10: 'recipient_registration_number',
         11: 'recipient_branch_number',
         12: 'recipient_business_name',
         13: 'recipient_representative_name',
         14: 'recipient_address',
         15: 'total_amount',
         16: 'supply_amount',
         17: 'tax_amount',
         18: 'electronic_invoice_classification',
         19: 'electronic_invoice_type',
         20: 'issuance_type',
         21: 'remarks',
         22: 'receipt_billing_division',
         23: 'supplier_email',
         24: 'recipient_email1',
         25: 'recipient_email2',
         26: 'item_date',
         27: 'item_name',
         28: 'item_specification',
         29: 'item_quantity',
         30: 'item_unit_price',
         31: 'item_supply_amount',
         32: 'item_tax_amount',
         33: 'item_remarks',
      }

            
      df.rename(columns=column_mapping, inplace=True)
      print(df)
      sales_data = df.to_dict('records')
      print(sales_data)
      def replace_comma(s):
         if isinstance(s, str):
            if s[0] == '-':
               return '-' + s[1:].replace(',', '')
            else:
               return s.replace(',', '')
         else:
            return s
      for sale_data in sales_data:
         for key, value in sale_data.items():
            if key.endswith(('amount', 'price', 'quantity')):  # 필요한 필드가 있으면 더 추가하세요
               try:
                  # 숫자로 변환 시도 (Decimal로 변환)
                  value = replace_comma(value)  # 쉼표 제거 함수 호출
                  sale_data[key] = Decimal(value)
                  if math.isnan(sale_data[key]):
                     sale_data[key] = None
               except (ValueError, TypeError):
                  sale_data[key] = None  # 변환 실패하면 None으로 설정
      # Purchase 객체를 일괄로 생성
      created_sales = []
      for data in sales_data:
         try:
            # 숫자로 변환 시도
            data['item_quantity'] = float(replace_comma(data['item_quantity']))  # 쉼표 제거 함수 호출
            if math.isnan(data['item_quantity']):
               data['item_quantity'] = None
         except (ValueError, TypeError):
            data['item_quantity'] = None  # 변환 실패하면 None으로 설정
         existing_sale = Sales.objects.filter(approval_number=data['approval_number']).first()
         if not existing_sale:
            # Purchase 객체 생성 후 리스트에 추가
            created_sales.append(Sales(**data))
      # bulk_create에 전달
      Sales.objects.bulk_create(created_sales)

      return redirect('sales:sales_UploadExcelForm')
   else:
      form = Sales_UploadExcelForm()

   return render(request, 'sales/sales_upload_excel.html', {'form': form})