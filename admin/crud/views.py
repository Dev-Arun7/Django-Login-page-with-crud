from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from crud.models import Employees
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.cache import never_cache

# Create your views here.

@cache_control(no_cache=True,must_revalidate=True, no_store=True)
@never_cache
def LoginPage(request):
     if 'username' in request.session:
         return redirect('home')
     if request.method=='POST':
         username=request.POST.get('username')
         pass1=request.POST.get('password')
         user=authenticate(request,username=username,password=pass1)
         if user is not None:
             request.session['username']=username
             login(request,user)
             return redirect('home')
         else:
             return HttpResponse("Invalid Username or Password")     
     return render(request,'login.html')

            
     


@login_required(login_url='login')
@cache_control(no_cache=True,must_revalidate=True, no_store=True)
def index(request):
    emp = Employees.objects.all()

    context = {
        'emp':emp,
    }
    if 'username' in request.session:
        return render(request,'index.html',context)
    return redirect('login')
#add page
def add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        emp = Employees(
            name = name,
            email = email,
            address = address,
            phone = phone
        )
        emp.save()
        return redirect('home')       
    return render(request,'index.html')


def edit(request):
    emp = Employees.objects.all()

    context = {
        'emp':emp,
    }
    return redirect(request,'index.html', context)
    


def update(request,id):
    if request.method == "POST": 
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        emp = Employees(
            id=id,
            name = name,
            email = email,
            address = address,
            phone = phone
         )
        emp.save()
        return redirect('home')
    return redirect(request,'index.html')


def delete(request,id):
    emp=Employees.objects.filter(id = id)
    emp.delete() 
    context = {
        'emp':emp,
    }
    return redirect('home')




def LogoutPage(request):
    if 'username' in request.session:
        request.session.flush()
    logout(request)
    return redirect('login')

    
def search(request):
    query=request.GET['query']
    emp = Employees.objects.filter(
        Q(name__icontains=query) | Q(phone__icontains=query) | Q(email__icontains=query) | Q(address__icontains=query)
          )
    context = {
        'emp':emp,       
    }
    return render(request, 'search.html',context)
    


   
