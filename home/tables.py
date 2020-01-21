import django_tables2 as tables
from django_tables2.utils import A
from django.utils.html import format_html
from django.urls import reverse
from django.urls import reverse_lazy
from .models import Unit_station_names, Loan_status, Loans, Customers, Repayments

class LoansTable(tables.Table):
	class Meta:
		model = Loans
		fields = ('loan_date','due_date','loan_code','loan_amount','customer_station','customer_id','loan_status')


class CustomersTable(tables.Table):
    customer_id = tables.LinkColumn(
    	'expand_customer', args=[A('customer_id')], verbose_name="Customer id:(Expand to loans demographics)", orderable=False, empty_values=())
    class Meta:
        model = Customers
        fields = ('customer_id', 'name', 'phone',
		          'created_at', 'loan_status','gender')


class RepaymentsTable(tables.Table):
	class Meta:
		model = Repayments
		fields = ('name', 'phone', 'loan_code', 'repayment_date','amount_paid')
