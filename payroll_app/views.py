from django.shortcuts import render, redirect, get_object_or_404
from .models import *
# Create your views here.
def employees(request):
    emp = Employee.objects.all()
    return render(request, 'lazapeeapp/employees.html', {'emp':emp})
    
def overtime(request, pk):
    if request.method == "POST":
        inp_o = request.POST.get("overtime")
        emp_r = Employee.objects.get(pk=pk).getRate()
        ot = (emp_r/160) * float(1.5) * float(inp_o) 
        Employee.objects.filter(pk=pk).update(overtime_pay=ot)
        return redirect('employees') 
    else:
        return redirect('employees') 
       
def create_employee(request):
    emp = Employee.objects.all()
    if request.method == "POST":
        n = request.POST.get('name')
        id = request.POST.get('idnum')
        r = request.POST.get('rate')
        a = request.POST.get('allowance')
        if a == "":
            a = 0
        
        Employee.objects.create(name=n, id_number=id, rate=r, allowance=a)
        return redirect('employees')
    else:
        return render(request, 'lazapeeapp/create_employee.html')

def delete_employee(request, pk):
    Employee.objects.filter(pk=pk).delete()
    return redirect('employees')

def update_employee(request):
    return render(request, 'lazapeeapp/update_employee')

# def test(request, pk):
#      Employee.objects.get(pk=pk).resetOvertime()
#      a = Employee.objects.get(pk=pk).getOvertime()
#      return redirect('employees')
