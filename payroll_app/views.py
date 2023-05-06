from django.shortcuts import render, redirect, get_object_or_404
from .models import *

# Create your views here.
def employees(request):
    emp = Employee.objects.all()
    return render(request, 'payroll_app/employees.html', {'emp':emp})
    
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
        return render(request, 'payroll_app/create_employee.html')

def delete_employee(request, pk):
    Employee.objects.filter(pk=pk).delete()
    return redirect('employees')

def update_employee(request, pk):
    emp = get_object_or_404(Employee, pk=pk)

    if(request.method=="POST"):
        n = request.POST.get('name')
        id = request.POST.get('idnum')
        r = request.POST.get('rate')
        a = request.POST.get('allowance')

        Employee.objects.filter(pk=pk).update(name=n, id_number=id, rate=r, allowance=a )
        return redirect('employees')
    else: 
        return render(request, 'payroll_app/update_employee.html', {'emp':emp})
    
def view_payslips(request):
    emp = Employee.objects.all()
    return render(request, 'payroll_app/payslips.html', {'emp':emp})

def payslip_submit(request):
    emp = Employee.objects.all()
    inp_for = request.POST.get('payslip_for')
    inp_month = request.POST.get('month')
    c = 0
    d = None
    inp_year = request.POST.get('year')
    month30 = ["4", "6", "9", "11"]
    leap_status = None
    inp_cycle = request.POST.get('cycle')

    # Leap year check
    if int(inp_year) % 4 == 0:
        if int(inp_year) % 100 == 0:
            if int(inp_year) % 400 == 0:
                leap_status = "LEAP!"
            else:
                leap_status = "NOT LEAP!"
        else:    
            leap_status = "LEAP!"
    else:
        leap_status = "NOT LEAP!"
 

    day_range = None

    if inp_cycle == "1":
        day_range = "1-15"
    if inp_cycle == "2":
        if inp_month in month30:
            day_range = "16-30"
        elif inp_month == "2":
            if leap_status == "LEAP!":
                day_range = "16-29"
            else:
                day_range = "16-28"
        else:
            day_range = "16-31"

    
    if inp_for != "all":
        active_id = Employee.objects.get(id_number=inp_for)
        gross_pay = active_id.getRate() + active_id.getAllowance() + active_id.getOvertime()
        philhealth = active_id.getRate() * 0.04
        sss = active_id * 0.045


    context = {
        'b':inp_month,
        'd':d,
        'l':leap_status,
        'r':day_range,
        'emp': emp,
    }


    # elif inp_for == "all":  
    #     for i in emp:
    #         c+=1 #replace with create payslip object  
    # else:
    #     pass

    # context = {
    #     'a': inp_for,
    #     'b': b,
    #     'c': c,
    #     'd': d,
    #     'e':gross_pay,
    # }

    
    

    return render(request, 'payroll_app/test.html', context)

# def test(request, pk):
#      Employee.objects.get(pk=pk).resetOvertime()
#      a = Employee.objects.get(pk=pk).getOvertime()
#      return redirect('employees')
