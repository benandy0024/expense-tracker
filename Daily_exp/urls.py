from django.conf.urls import url
from .views import expense_create,expense_list,update_expense,home,expense_list_json
urlpatterns = [
    url('expense-json', expense_list_json,name='expense_list_api'),
    url('expense-create/', expense_create),
    url('expense/', expense_list,name='list'),
url(r'update/(?P<id>[\w-]+)/$', update_expense, name='update'),

]