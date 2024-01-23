from django.db import models

import math
import re

# Create your models here.
class Sales(models.Model):
   written_date = models.DateField(null=True, blank=True) #작성일자 (Date of Writing): written_date
   approval_number = models.CharField(max_length=255, null=True, blank=True) #승인번호 (Approval Number): approval_number
   issue_date = models.DateField(null=True, blank=True) #발급일자 (Date of Issuance): issue_date
   transmission_date = models.DateField(null=True, blank=True) #전송일자 (Date of Transmission): transmission_date
   supplier_registration_number = models.CharField(max_length=255, null=True, blank=True) #공급자사업자등록번호 (Supplier's Business Registration Number): supplier_registration_number
   supplier_branch_number = models.CharField(max_length=255, null=True, blank=True) #종사업장번호 (Supplier's Business Branch Number): supplier_branch_number
   supplier_business_name = models.CharField(max_length=255, null=True, blank=True) #상호 (Supplier's Business Name): supplier_business_name
   supplier_representative_name = models.CharField(max_length=255, null=True, blank=True) #대표자명 (Representative Name): supplier_representative_name
   supplier_address = models.CharField(max_length=255, null=True, blank=True) #주소 (Supplier's Address): supplier_address
   recipient_registration_number = models.CharField(max_length=255, null=True, blank=True) #공급받는자사업자등록번호 (Recipient's Business Registration Number): recipient_registration_number
   recipient_branch_number = models.CharField(max_length=255, null=True, blank=True) #종사업장번호 (Recipient's Business Branch Number): recipient_branch_number
   recipient_business_name = models.CharField(max_length=255, null=True, blank=True) #상호 (Recipient's Business Name): recipient_business_name
   recipient_representative_name = models.CharField(max_length=255, null=True, blank=True) #대표자명 (Recipient's Representative Name): recipient_representative_name
   recipient_address = models.CharField(max_length=255, null=True, blank=True) #주소 (Recipient's Address): recipient_address
   total_amount = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True) #합계금액 (Total Amount): total_amount
   supply_amount = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True) #공급가액 (Supply Amount): supply_amount
   tax_amount = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True) #세액 (Tax Amount): tax_amount
   electronic_invoice_classification = models.CharField(max_length=255, null=True, blank=True) #전자세금계산서분류 (Electronic Tax Invoice Classification): electronic_invoice_classification
   electronic_invoice_type = models.CharField(max_length=255, null=True, blank=True) #전자세금계산서종류 (Electronic Tax Invoice Type): electronic_invoice_type
   issuance_type = models.CharField(max_length=255, null=True, blank=True) #발급유형 (Issuance Type): issuance_type
   remarks = models.TextField(null=True, blank=True) #비고 (Remarks): remarks
   receipt_billing_division = models.CharField(max_length=255, null=True, blank=True) #영수/청구 구분 (Receipt/Billing Division): receipt_billing_division
   supplier_email = models.EmailField(null=True, blank=True) #공급자 이메일 (Supplier's Email): supplier_email
   recipient_email1 = models.EmailField(null=True, blank=True) #공급받는자 이메일1 (Recipient's Email 1): recipient_email1
   recipient_email2 = models.EmailField(null=True, blank=True) #공급받는자 이메일2 (Recipient's Email 2): recipient_email2
   item_date = models.DateField(null=True, blank=True) #품목일자 (Item Date): item_date
   item_name = models.CharField(max_length=255, null=True, blank=True) #품목명 (Item Name): item_name
   item_specification = models.CharField(max_length=255, null=True, blank=True) #품목규격 (Item Specification): item_specification
   item_quantity = models.FloatField(null=True, blank=True) #품목수량 (Item Quantity): item_quantity
   item_unit_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True) #품목단가 (Item Unit Price): item_unit_price
   item_supply_amount = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True) #품목공급가액 (Item Supply Amount): item_supply_amount
   item_tax_amount = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True) #품목세액 (Item Tax Amount): item_tax_amount
   item_remarks = models.TextField(null=True, blank=True) #품목비고 (Item Remarks): item_remarks

   def clean_quantity(self, value):
      try:
         # 콤마 제거하고 숫자로 변환
         cleaned_value = float(re.sub(r'[^\d.]', '', str(value)))
         return cleaned_value
      except ValueError:
            return None

   def save(self, *args, **kwargs):
      # 'item_quantity' 필드에 들어가는 값이 NaN일 경우 None으로 처리
      if math.isnan(self.item_quantity):
               self.item_quantity = None

      super().save(*args, **kwargs)


   def __str__(self):
      return str(self.approval_number)