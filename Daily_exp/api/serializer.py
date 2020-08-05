from rest_framework import serializers
from Daily_exp.models import Expense,Income


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model=Expense
        fields=['id','user','item','amount']
        read_only_field=['user']


class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model=Income
        fields=['income_amount']
        read_only_field=['user']