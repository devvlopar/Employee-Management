from datetime import datetime
from multiprocessing import context
from urllib import response
from django.shortcuts import render,HttpResponse
from .models import Employee,Role,Department
from datetime import datetime
from django.db.models import Q

# Create your views here.

def index(request):
    return render(request,'index.html')

def all_emp(request):
    emps = Employee.objects.all()
    print("hello")
    context = {

        'emps': emps 

    }
    
        
    return render(request,'view_all_emp.html',context)

def add_emp(request):

    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        salary=request.POST['salary']
        bonus=request.POST['bonus']
        phone=int(request.POST['phone'])
        role=Role.objects.get(id=request.POST['role'])
        department = role.department
       
        
        new_emp = Employee.objects.create(
            first_name = first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            phone=phone,
            department=department,
            role=role,
            hire_date=datetime.now()
        )
        

        return HttpResponse("Employee add succesfully")
    elif request.method=="GET":
        a_d = Department.objects.all()
        all_roles = Role.objects.all()
        return render(request,'add_emp.html',{'all_departments':a_d, 'all_roles':all_roles})
    else:
        return HttpResponse("an exceptional occurred employee has not add" )  

def remove_emp(request,emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed=Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee removed successfully")
        except:
            return HttpResponse("please enter valid emp id")    
    emps=Employee.objects.all()
    context = {
    'emps': emps

    }
    return render(request,'remove_emp.html',context)

def filter_emp(request):
    if request.method =="POST":
        name=request.POST["first_name"]
        department=request.POST["department"]
        role=request.POST["role"]
        emps=Employee.objects.all()
        print(department,role)
        if len(department) ==0 and len(role) == 0:
            emps=emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        elif len(department) >= 1 and len(name) >= 1:
            emps=emps.filter(department__name__icontains=department).filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        elif len(role) >= 1 and len(name) >= 1:
            emps=emps.filter(role__name__icontains=role).filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        else:
            emps=emps.filter(department__name__icontains=department, role__name__icontains=role)
        context ={
            'emps':emps
        }    
        return render(request,"view_all_emp.html",context)
    elif request.method=="GET":   
        data1 = {
            'all_roles': Role.objects.all(),
            'all_departments' : Department.objects.all()
        }
        return render(request,'filter_emp.html',data1)  
    else:
        return HttpResponse("Exceptional Occured")          
    
            
