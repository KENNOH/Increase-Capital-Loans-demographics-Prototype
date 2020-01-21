from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_protect
from django_tables2 import RequestConfig
from .forms import UploadFileForm
from django.contrib import messages
from django.utils.datastructures import MultiValueDictKeyError
from pyexcel_xlsx import get_data as xlsx_get
from pyexcel_xls import get_data as xls_get
from django.shortcuts import redirect
from django.urls import path
from .models import Unit_station_names, Loan_status, Loans , Customers,Repayments
from .tables import LoansTable, CustomersTable, RepaymentsTable
import datetime
from django.db.models import Q
from xhtml2pdf import pisa
from .utils import render_to_pdf
from django.http import HttpResponse
import csv
from .render import Render

# Create your views here.

#shows the landing page
def home(request):
	return render(request, 'home/app.html')


#this controller handles the excel loans data sheet
#note that this can be a long running task and might take time depending on the size of the excel dataset
#It took approximately 45 minutes to process all the 80,913 records.
#i recommend that such tasks be delegated to celery(a background task queue to improve efficiency)
def upload(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			try:
				excel_file = request.FILES['files']
				if (str(excel_file).split('.')[-1] == "xls"):
					data = xls_get(excel_file, column_limit=7)
				elif (str(excel_file).split('.')[-1] == "xlsx"):
					data = xlsx_get(excel_file, column_limit=7)
				unit_stations = data["unit_station_names"]
				loan_status = data["loan_status"]
				loans = data["loans"]

				#adding unit stations data to the database
				if (len(unit_stations)>2):
					for i in range(1,len(unit_stations)):
						#to avoid making duplicate records
						if not Unit_station_names.objects.filter(station_name=unit_stations[i][1]):
							Unit_station_names.objects.create(station_name=unit_stations[i][1], daily_target=unit_stations[i][2], monthly_target=unit_stations[i][3])
						else:
						#to update only the daily target and monthly target values that have changed
							station = Unit_station_names.objects.get(station_name = unit_stations[i][1])
							station.daily_target = unit_stations[i][2]
							station.monthly_target = unit_stations[i][3]
							station.save()

				#adding loan status data to the database
				if (len(loan_status) > 2):
					for j in range(1, len(loan_status)):
						#to avoid making duplicate records
						if not Loan_status.objects.filter(loan_status=loan_status[j][1]):
							Loan_status.objects.create(loan_status=loan_status[j][1])
				
				#adding loans data to the database
				if (len(loans) > 2):
					for k in range(1, len(loans)):
						#to avoid making duplicate records
						if not Loans.objects.filter(loan_code=loans[k][2]):
							station = Unit_station_names.objects.get(id=loans[k][4])
							status = Loan_status.objects.get(id=loans[k][6])
							Loans.objects.create(
								loan_date=loans[k][0],
								due_date=loans[k][1],
								loan_code=loans[k][2],
								loan_amount=loans[k][3],
								customer_station=station,
								customer_id=loans[k][5],
								loan_status=status)
				messages.info(request, 'Processed successfully!!!')
				return HttpResponseRedirect('/upload/')
			except:
				#used to raise exceptions if the excel document is not formatted properly
				messages.info(request, 'This is not a valid document for the above process')
				return HttpResponseRedirect('/upload/')
		else:
			messages.info(
				request, 'The was an error processing your upload.Check your excel file.')
			return HttpResponseRedirect('/upload/')
	else:
		form = UploadFileForm()
		return render(request, 'home/upload.html',{'form':form})
 
#shows the loans data page
def display(request):
	now = datetime.datetime.now()
	count = Loans.objects.all().count()
	assets = LoansTable(Loans.objects.all())
	RequestConfig(request, paginate={"per_page": 20}).configure(assets)
	return render(request, 'home/loans.html', {'assets': assets,'count':count,'now':now})

#shows the customers page
def customers(request):
	now = datetime.datetime.now()
	count = Customers.objects.all().count()
	cust = CustomersTable(Customers.objects.all())
	RequestConfig(request, paginate={"per_page": 20}).configure(cust)
	return render(request, 'home/customers.html', {'cust': cust, 'count': count, 'now': now})

#shows the loan repayments data page
def repayments(request):
	now = datetime.datetime.now()
	count = Repayments.objects.all().count()
	repay = RepaymentsTable(Repayments.objects.all())
	RequestConfig(request, paginate={"per_page": 20}).configure(repay)
	return render(request, 'home/repayments.html', {'repay': repay, 'count': count, 'now': now})


#shows the individual loan records as per each customer and the repayments records page
def expand_customer(request, customer_id):
	loans = Loans.objects.all().filter(customer_id=customer_id)
	data = []
	for i in loans:
		data.append(i)
	repayments = Repayments.objects.all().filter(loan_code__in=data)
	
	assets = LoansTable(loans)
	RequestConfig(request, paginate={"per_page": 5}).configure(assets)
	repay = RepaymentsTable(repayments)
	RequestConfig(request, paginate={"per_page": 5}).configure(repay)
	loan_count = loans.count()
	repay_count = repayments.count()
	now = datetime.datetime.now()
	c = Customers.objects.all().get(customer_id=customer_id)
	return render(request, 'home/expand_customer.html', {'repay': repay,'assets': assets,'loan_count':loan_count,'repay_count':repay_count,'now': now,'c':c})


def process_filter(request):
	if request.method == "POST":
		date1 = request.POST['startdate']
		date2 = request.POST['enddate']
		hidden = request.POST['hidden'] #hidden input to help know which input should be used
		s = datetime.datetime.strptime(date1, "%Y-%m-%d").date()#formatting date before processing
		t = datetime.datetime.strptime(date2, "%Y-%m-%d").date()
		now = datetime.datetime.now()

		#to know if the export to excel button has been pressed
		if 'excel' in request.POST:
			return export_to_excel(s,t,hidden) #runs the export to pdf function

		#to know if the export to excel button has been pressed
		if 'pdf' in request.POST:
			return export_to_pdf(s,t,hidden)  #runs the export to pdf function

		#filters the loans table
		if hidden=='loans':
			count = Loans.objects.all().filter(loan_date__range=[s, t]).count()
			assets = LoansTable(Loans.objects.all().filter(loan_date__range=[s, t]))
			RequestConfig(request, paginate={"per_page": 20}).configure(assets)
			messages.info(request, 'Showing loans issued between ' + date1 + " and " + date2 + " ,filtered according to loan date.")
			return render(request, 'home/loans.html', {'assets': assets, 'count': count, 'now': now})
		#filters the customers table
		if hidden=='customers':
			count = Customers.objects.all().filter(created_at__range=[s, t]).count()
			cust = CustomersTable(Customers.objects.all().filter(created_at__range=[s, t]))
			RequestConfig(request, paginate={"per_page": 20}).configure(cust)
			messages.info(request, 'Showing customers registered between ' + date1 + " and " + date2 + " ,filtered according to created date.")
			return export_to_excel(s, t, hidden)
			return render(request, 'home/customers.html', {'cust': cust, 'count': count, 'now': now})
		#filters the repayments table
		if hidden=='repayments':
			count = Repayments.objects.all().filter(repayment_date__range=[s, t]).count()
			repay = RepaymentsTable(Repayments.objects.all().filter(repayment_date__range=[s, t]))
			RequestConfig(request, paginate={"per_page": 20}).configure(repay)
			messages.info(request, 'Showing repayments issued between ' + date1 + " and " + date2 + " ,filtered according to loan repayment date")
			return render(request, 'home/repayments.html', {'repay': repay, 'count': count, 'now': now})
	else:
		return HttpResponseRedirect('/')


#this functions deals with exporting the dataset to excel document
def export_to_excel(s,t,hidden):
	#handles the customers table
	if hidden=='customers':
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="customers.csv"'
		writer = csv.writer(response)
		writer.writerow(['name', 'phone','email','customer_id','gender','loan_status','created_at'])
		assets = Customers.objects.all().filter(created_at__range=[s, t]).values_list(
			'name', 'phone', 'email', 'customer_id', 'gender', 'loan_status', 'created_at').order_by('-created_at')
		for i in assets:
			writer.writerow(i)
		return response

	#handles the loans table
	if hidden == 'loans':
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="loans.csv"'
		writer = csv.writer(response)
		writer.writerow(['customer_id', 'customer_station', 'loan_status', 'loan_amount','loan_code','loan_date','due_date'])
		assets = Loans.objects.all().filter(loan_date__range=[s, t]).values_list(
			'customer_id', 'customer_station', 'loan_status', 'loan_amount', 'loan_code', 'loan_date', 'due_date').order_by('-loan_date')
		for i in assets:
			writer.writerow(i)
		return response

	#handles the repayments table
	if hidden == 'repayments':
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="repayments.csv"'
		writer = csv.writer(response)
		writer.writerow(['name', 'phone', 'loan_code',
                   'repayment_date', 'amount_paid'])
		assets = Repayments.objects.all().filter(repayment_date__range=[s, t]).values_list(
			'name', 'phone', 'loan_code', 'repayment_date', 'amount_paid').order_by('-repayment_date')
		for i in assets:
			writer.writerow(i)
		return response


#this functions deals with exporting the dataset to a pdf document
def export_to_pdf(s, t, hidden):
	if hidden == 'customers':
		customers = Customers.objects.all().filter(created_at__range=[s, t])
		return Render.render('home/customers_pdf.html', {'customers': customers})
	if hidden == 'loans':
		loans = Loans.objects.all().filter(loan_date__range=[s, t])
		return Render.render('home/loans_pdf.html', {'customers': loans})
	if hidden == 'repayments':
		repayments = Repayments.objects.all().filter(repayment_date__range=[s, t])
		return Render.render('home/repayments_pdf.html', {'customers': repayments})
	




def search(request):
	if request.method == "POST":
		search_text = request.POST['search_loan']
		hidden = request.POST['hidden']
		now = datetime.datetime.now()
		if search_text != '':
			#searches the loans table
			if hidden == 'loans':
				count = Loans.objects.all().filter(Q(customer_id=search_text)| Q(loan_code=search_text)).count()
				assets = LoansTable(Loans.objects.all().filter(Q(customer_id=search_text) | Q(loan_code=search_text)))
				RequestConfig(request, paginate={"per_page": 20}).configure(assets)
				messages.info(request, 'Showing loans issued according to keyword. ' + search_text)
				return render(request, 'home/loans.html', {'assets': assets, 'count': count, 'now': now})
			#searches the customers table
			if hidden == 'customers':
				count = Customers.objects.all().filter(Q(name__icontains=search_text) | Q(phone=search_text)
				| Q(customer_id=search_text) | Q(email__in=search_text)).count()
				cust = CustomersTable(Customers.objects.all().filter(Q(name__icontains=search_text) | Q(
				phone=search_text) | Q(customer_id=search_text) | Q(email=search_text)))
				RequestConfig(request, paginate={"per_page": 20}).configure(cust)
				messages.info(request, 'Showing customers according to keyword. ' + search_text)
				return render(request, 'home/customers.html', {'cust': cust, 'count': count, 'now': now})
			#searches the repayments table
			if hidden == 'repayments':
				count = Repayments.objects.all().filter(Q(phone=search_text) | Q(amount_paid=search_text)).count()
				repay = RepaymentsTable(Repayments.objects.all().filter(Q(phone=search_text) | Q(amount_paid=search_text)))
				RequestConfig(request, paginate={"per_page": 20}).configure(repay)
				messages.info(request, 'Showing repayments issued according to keyword. ' + search_text)
				return render(request, 'home/repayments.html', {'repay': repay, 'count': count, 'now': now})
		else:
			return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/')

