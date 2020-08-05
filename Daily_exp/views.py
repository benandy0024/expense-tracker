import datetime
import json
import random
from django.shortcuts import render,redirect
from.forms import ExpenseForm
from.models import Expense,Income
from django.http import JsonResponse
from django.utils import timezone
# Create your views here.
def home(request):
    return render(request,'home.html')
def expense_list_json(request):
    data={}
    qs = Expense.objects.all().recent().by_weeks_range(weeks_ago=10, numbers_of_weeks=10)
    day_qs=Expense.objects.filter(user=request.user).by_date()
    if request.GET.get('type')=="week":
        days=7
        start_date=timezone.now().today()-datetime.timedelta(days=days-1)
        datetime_list=[]
        labels=[]
        expense_data=[ ]
        for x in range(0,days):
            new_time= start_date+datetime.timedelta(days=x)
            datetime_list.append(
               new_time
            )
            labels.append(
                new_time.strftime("%a")
            )
            new_qs=qs.filter(timestamp__day=new_time.day,timestamp__month=new_time.month)
            day_total=new_qs.total_data()['amount__sum']
            if day_total is None:
                day_total=0
            expense_data.append(
                day_total
            )

        data['labels']=labels
        data['data']=expense_data
    if request.GET.get('type') == "today":
        items = []
        price=[]
        for x in day_qs:
         items.append(str(x))
         price.append(x.amount)
         data['labels'] = items
         data['data'] = price
    return JsonResponse(data)
def expense_list(request):
    # expense query_set
    qs=Expense.objects.all().recent().by_weeks_range(weeks_ago=10,numbers_of_weeks=10)
    today_qs=qs.filter(user=request.user).by_date()

    this_week_qs=qs.filter(user=request.user).by_weeks_range(weeks_ago=1,numbers_of_weeks=1).get_expense_breakdown()
    last4_week_qs = qs.filter(user=request.user).by_weeks_range(weeks_ago=4, numbers_of_weeks=4).get_expense_breakdown()

    # income query_set
    income_qs=Income.objects.filter(user=request.user).total_income_by_date()

    context={"this_week":this_week_qs,
             "today_qs":today_qs,
             "last4_week": last4_week_qs,

             "income_qs":income_qs,

             }
    return render(request,'expenses/list.html',context)
def expense_create(request):
    exp_form = ExpenseForm(request.POST)
    if request.method=="POST":
        if exp_form.is_valid():
            instance = exp_form.save()
            instance.user = request.user
            instance.save()
    else:
        exp_form=ExpenseForm()
    context={'exp_form':exp_form}
    return render(request,'expenses/create.html',context)


def update_expense(request,id):
    exp_form=Expense.objects.get(id=id)
    form = ExpenseForm(instance=exp_form)
    if request.method=="POST":
        form = ExpenseForm(request.POST, instance=exp_form)
        if form.is_valid():
            form.save()
            return redirect('daily_expense:list')
        form=ExpenseForm()
    context={'form':form}
    return render(request,'expenses/update.html',context)

