from rest_framework import generics,mixins
from rest_framework.response import Response
from Daily_exp.models import Expense,Income
from .serializer import ExpenseSerializer,IncomeSerializer
from rest_framework.views import APIView
from django.db.models import Sum,Avg,Count
class ExpenseListView(APIView):
    def get(self,request):
        qs=Expense.objects.all().recent()
        serializer=ExpenseSerializer(qs,many=True)
        return Response(serializer.data)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
#get the week expenses
class ExpenseByWeek(APIView):

    def get(self,request):
        qs = Expense.objects.all().recent().by_weeks_range(weeks_ago=10,numbers_of_weeks=10)
        exp_qs = qs.filter(user=request.user).by_weeks_range()
        serializer = ExpenseSerializer(exp_qs, many=True)

        all_sum = exp_qs.aggregate(Sum('amount'))['amount__sum']
        return Response({'sum': all_sum if all_sum else 0, 'objects': serializer.data})

#get the day expenses
class ExpenseByDay(APIView):
    def get(self,request):
        qs = Expense.objects.all().recent()
        exp_qs = qs.filter(user=request.user).by_date()
        serializer = ExpenseSerializer(exp_qs, many=True)

        all_sum = exp_qs.aggregate(Sum('amount'))['amount__sum']
        return Response({'sum': all_sum if all_sum else 0, 'objects': serializer.data})
#income qs
class IncomeListView(APIView):
    def get(self,request):
        qs=Income.objects.all().total_income_by_date()
        income_qs = qs.filter(user=request.user)
        serializer=IncomeSerializer(income_qs,many=True)
        return Response(serializer.data)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
# update expense
class ExpenseUpdate(mixins.UpdateModelMixin,generics.RetrieveAPIView):
    serializer_class =ExpenseSerializer
    lookup_field = "id"
    def get_queryset(self):
        qs=Expense.objects.all()
        return qs
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

