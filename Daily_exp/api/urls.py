from django.conf.urls import url
from .views import ExpenseByWeek,ExpenseUpdate,ExpenseListView,ExpenseByDay,IncomeListView
urlpatterns = [
    url('expense-list', ExpenseListView.as_view(), name='list-api'),
    url('expense-day', ExpenseByDay.as_view(), name='day-list-api'),
    url('expense-week',ExpenseByWeek.as_view(),name='week-list-api'),
url('income',IncomeListView.as_view(),name='amount-api'),
 url(r'updates/(?P<id>[\w-]+)/$', ExpenseUpdate.as_view(), name='update-api'),

]