from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def home(request):
    return render(request,'index.html')

def signup(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    context={
        'form':form
    }
    return render(request,'registration/signup.html',context)