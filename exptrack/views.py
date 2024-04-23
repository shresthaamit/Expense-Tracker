import decimal
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, LoginForm,IncomeForm,ExpenseForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from.models import Income, Expenses
from decimal import Decimal
from django import forms
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import HttpResponse
import json
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from collections import defaultdict

# Create your views here.
from .models import *
def registerpage(request):
    if request.method  == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request,'register.html',{'form':form})

def loginpage(request):
    user = CustomUserCreationForm()
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print("Email:", email) 
            print("Password:", password)
            user = authenticate(request, email= email, password=password)
            # print("Email:", emails) 
            print("Password:", password)
            print("User:", user)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request,f'Invalid username or password')  
        
    return render(request, 'login.html',{'form':form})

def logoutpage(request):
    logout(request)
    return redirect('login')

def password_reset(request):
    return render(request, 'password_reset.html')

def password_reset_done(request):
    return render(request, 'password_reset_done.html')

def password_reset_confirm(request):
    return render(request, 'password_reset_confirm.html')

def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')
class DecimalEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super().default(o)
def home(request):
    alldata =getcombine(request)
    monthly_summary = defaultdict(lambda: {'income': 0, 'expenses': 0})

    for data in alldata:
        month = data.date.strftime("%B")
        total_amount = sum(getattr(data, f'source_{i}_amount', 0) or 0 for i in range(1, 4))
        if isinstance(data, Income):
            monthly_summary[month]['income'] += total_amount
        elif isinstance(data, Expenses):
            monthly_summary[month]['expenses'] += total_amount
    serialized_data = json.dumps(dict(monthly_summary),cls=DecimalEncoder) 
    # Print monthly summary
    for month, summary in monthly_summary.items():
        print(f"Month: {month}")
        print(f"Income: {summary['income']}")
        print(f"Expenses: {summary['expenses']}")

    # monthly_summary = defaultdict(dict)
    # for data in alldata:
    #     month = data.date.strftime("%B")
    #     if isinstance(data, Income):
    #         total_amount = sum(getattr(data, f'source_{i}_amount', Decimal('0')) or Decimal('0') for i in range(1, 4))
    #         monthly_summary[month]['income'] = monthly_summary[month].get('income', Decimal('0')) + total_amount
    #     elif isinstance(data, Expenses):
    #         total_amount = sum(getattr(data, f'source_{i}_amount', Decimal('0')) or Decimal('0') for i in range(1, 4))
    #         monthly_summary[month]['expenses'] = monthly_summary[month].get('expenses', Decimal('0')) + total_amount
    # alldatas = [data for data in alldata if data.date.strftime("%B").lower()]
    totalincome = calculateIncome(request)
    totalexpense = calculateExpenses(request)
    totalsave = calculateSave(request)
    print(alldata)
    return render(request, 'index.html', {'totalincome':totalincome,'totalexpense':totalexpense,'totalsave':totalsave,'monthly_summary': serialized_data})

def profilewallet(request):
    return render(request,'profile.html',{})

@login_required(login_url='login')
def incomeform(request):
    current_user = request.user
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.instance.user = current_user
            form.save()
            print("Saved")
            form=IncomeForm()   
    else:
        form = IncomeForm(initial={'user': current_user})
    return render(request,'incomeform.html',{'form':form})
def editIncome(request,id):
    current_user = request.user
    income = Income.objects.get(id=id, user=current_user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income,user=current_user)
        if form.is_valid():
            form.instance.user = current_user
            form.save()
            print("Income updated by user:", current_user.username)
            return redirect('showrecord')
        else:
            print(form.errors)
    else:
        form = IncomeForm(instance=income) 
        form.initial['user'] = current_user
        form.fields['user'].widget = forms.HiddenInput()
    return render(request,'incomeform.html',{'form':form,'income_id': id})
def deleteIncome(request, id):
    current_user = request.user
    income = Income.objects.get(id=id, user=current_user)
    income.delete()
    print("Income deleted by: ", current_user.username)
    return redirect('showrecord')
    # return render(request, 'record.html', {})  
def calculateIncome(request):
    # userincome = Income.objects.filter(user=request.user)
    userincome = Income.objects.filter(user=request.user)
    totalincome = Decimal('0.00')
    if userincome.exists():
        for income in userincome:
            totalincome += (income.source_1_amount or Decimal('0')) + (income.source_2_amount or Decimal('0')) + (income.source_3_amount or Decimal('0'))
    else:
        totalincome = Decimal('0.00')
    return totalincome

@login_required(login_url='login')
def expensesform(request):
    current_user = request.user
    if request.method == 'POST':
        form =ExpenseForm(request.POST)
        if form.is_valid():
            form.instance.user = current_user
            form.save()
            form=IncomeForm() 
    else:
        form = ExpenseForm(initial={'name': current_user.username})
    return render(request,'expenseform.html',{'form':form})

def editExpenses(request,id):
    current_user = request.user
    expenses =Expenses.objects.get(id=id, user=current_user)
    if request.method == "POST":
        form= ExpenseForm(request.POST, instance = expenses, user=current_user)
        if form.is_valid():
            form.instance.user = current_user
            form.save()
            print("Expenses edited by: ", current_user.username)
            return redirect('showrecord')
        else:
            print(form.errors)
    else:
        form =ExpenseForm(instance=expenses)
        form.initial['user'] = current_user
        form.fields['user'].widget = forms.HiddenInput()     
    return render(request, 'expenseform.html',{'form':form,  'expense_id': id}) 
   
def deleteExpenses(request,id):
    currentuser = request.user
    expenses = Expenses.objects.get(id=id,user = currentuser)
    expenses.delete()
    return redirect('showrecord')            
       
    
def calculateExpenses(request):
    userexpenses = Expenses.objects.filter(user= request.user)
    totalExpenses = Decimal('0.00')
    if userexpenses.exists():
        for expense in userexpenses:
            totalExpenses +=  (expense.source_1_amount or Decimal('0')) + (expense.source_2_amount or Decimal('0')) + (expense.source_3_amount or Decimal('0'))
            
    return totalExpenses

def getcombine(request):
    user = request.user
    allincome = Income.objects.filter(user=user).exclude(source_1_name=None, source_1_amount=0).exclude(source_2_name=None, source_2_amount=0).exclude(source_3_name=None, source_3_amount=0)
    allexpense = Expenses.objects.filter(user=user).exclude(source_1_name=None, source_1_amount=0).exclude(source_2_name=None, source_2_amount=0).exclude(source_3_name=None, source_3_amount=0).select_related('user')
    return list(allincome) + list(allexpense)
def showrecord(request):
    
    alldatas = getcombine(request)[:4]
    return render(request, 'record.html',{'alldatas':alldatas})

def calculateSave(request):
    calculatesave = calculateIncome(request) - calculateExpenses(request)
    return calculatesave

def allhistory(request):
    search_month = request.GET.get("search")
    alldata =getcombine(request)
    if search_month:
       
        alldata = [data for data in alldata if data.date.strftime("%B").lower() == search_month.lower()]
    paginator = Paginator(alldata,4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'history.html',{'alldata':alldata,'page_obj':page_obj})

def generatepdf(request):
    alldata =getcombine(request)
    # data = getcombine(request)

    # Create a response object
    companyname = "Expense Tracker:Developed by Shrestha"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="financial_history.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    company_name_style = styles["Title"]
    company_name_paragraph = Paragraph(companyname, company_name_style)
    elements.append(company_name_paragraph)

    elements.append(Paragraph("<br/>", company_name_style))
    # Define table data
    table_data = [
        ["Transaction", "Source", "Amount", "Date"],
        # Populate the table with your data
        # For example:
        *[[
            data.category,
            ', '.join([data.source_1_name, data.source_2_name, data.source_3_name]),
            ', '.join([str(data.source_1_amount), str(data.source_2_amount), str(data.source_3_amount)]),
            str(data.date)
        ] for data in alldata]
    ]

    table = Table(table_data)

    # Apply styles to the table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)

    # Add the table to the document
   
    elements.append(table)

   
    doc.build(elements)

    return response
    # alldata = getcombine(request)
    # tohtml = render_to_string('pdf_template.html', {'alldata': alldata})
    # topdf = pdfkit.from_string(tohtml,False)
    # response = HttpResponse(topdf,content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="financial_history.pdf"'
    # return response

def yearly_summary(request):
    alldata = getcombine(request)
    yearly_summary_data = {}


    for data in alldata:

        year = data.date.year

        if year not in yearly_summary_data:
            yearly_summary_data[year] = {'income': 0, 'expenses': 0}

        if isinstance(data, Income):
            yearly_summary_data[year]['income'] += (data.source_1_amount or 0) + \
                                                   (data.source_2_amount or 0) + \
                                                   (data.source_3_amount or 0)
        elif isinstance(data, Expenses):
            yearly_summary_data[year]['expenses'] += (data.source_1_amount or 0) + \
                                                      (data.source_2_amount or 0) + \
                                                      (data.source_3_amount or 0)

    return render(request, 'yearly_summary.html', {'yearly_summary_datas': yearly_summary_data})