from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
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
            a = None

        if Employee.objects.filter(id_number=id).exists():
            messages.error(request, "An employee with this ID number already exists")
            return redirect('create_employee')
        
        else:
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

        if Employee.objects.get(id_number=id).getID() == id:
            Employee.objects.filter(pk=pk).update(name=n, id_number=id, rate=r, allowance=a)
            return redirect('employees')
        
        elif Employee.objects.filter(id_number=id).exists():
            messages.error(request, "An employee with this ID number already exists")
            return redirect('update_employee', pk=pk)
        
        else:
            Employee.objects.filter(pk=pk).update(name=n, id_number=id, rate=r, allowance=a)
            return redirect('employees')
    else: 
        return render(request, 'payroll_app/update_employee.html', {'emp':emp})
    
def payslips(request):
    emp = Employee.objects.all()
    payslip_test = Payslip.objects.all()
    return render(request, 'payroll_app/payslips.html', {'emp':emp, 'ptest':payslip_test,})


def payslip_submit(request):
    if request.method == "POST":
        emp = Employee.objects.all()
        inp_for = request.POST.get('payslip_for')
        inp_month = request.POST.get('month')
        inp_year = request.POST.get('year')
        month30 = ["4", "6", "9", "11"]
        leap_status = None
        day_range = None
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
            payslip_test = Payslip.objects.all()
            base_pay = active_id.getRate()/2
            gross_pay = base_pay + active_id.getAllowance() + active_id.getOvertime()

            if inp_cycle == "2":
                philhealth = active_id.getRate() * 0.04
                sss = active_id.getRate() * 0.045
                tax = (gross_pay - sss - philhealth) * 0.2
                total_deductions = tax + sss + philhealth
                net_pay = gross_pay - total_deductions
                pag_ibig = 0
            else:
                philhealth = 0
                sss = 0
                pag_ibig = 100
                tax = (gross_pay - pag_ibig)*0.2
                total_deductions = tax + pag_ibig
                net_pay = gross_pay - total_deductions

            
            Payslip.objects.create(id_number=active_id,
                                month=inp_month,
                                date_range=day_range,
                                year=inp_year,
                                pay_cycle=inp_cycle,
                                rate=active_id.getRate(),
                                earnings_allowance=active_id.getAllowance(),
                                deductions_tax=tax,
                                deductions_health=philhealth,
                                pag_ibig=pag_ibig,
                                sss=sss,
                                overtime=active_id.getOvertime(),
                                total_pay=net_pay,
                                )
            active_id.resetOvertime()
            

            return redirect('payslips')
        else:
            payslip_test = Payslip.objects.all()
            for e in emp:
                active_id = e
                base_pay = active_id.getRate()/2
                gross_pay = base_pay + active_id.getAllowance() + active_id.getOvertime()

                if inp_cycle == "2":
                    philhealth = active_id.getRate() * 0.04
                    sss = active_id.getRate() * 0.045
                    tax = (gross_pay - sss - philhealth) * 0.2
                    total_deductions = tax + sss + philhealth
                    net_pay = gross_pay - total_deductions
                    pag_ibig = 0
                else:
                    philhealth = 0
                    sss = 0
                    pag_ibig = 100
                    tax = (gross_pay - pag_ibig)*0.2
                    total_deductions = tax + pag_ibig
                    net_pay = gross_pay - total_deductions

                
                Payslip.objects.create(id_number=active_id,
                                month=inp_month,
                                date_range=day_range,
                                year=inp_year,
                                pay_cycle=inp_cycle,
                                rate=active_id.getRate(),
                                earnings_allowance=active_id.getAllowance(),
                                deductions_tax=tax,
                                deductions_health=philhealth,
                                pag_ibig=pag_ibig,
                                sss=sss,
                                overtime=active_id.getOvertime(),
                                total_pay=net_pay,
                                )
                active_id.resetOvertime()
            return redirect('payslips')
      
    else:
        messages.error(request, 'Error!')
        return redirect('payslips')

def view_payslip(request, pk):
    d = get_object_or_404(Payslip, pk=pk)
    earnings = d.getCycleRate() + d.getEarnings_allowance() + d.getOvertime()
    deductions = d.getPag_ibig() + d.getDeductions_health() + d.getDeductions_tax() + d.getSSS()

    context = {
        'd': d,
        'earnings':earnings,
        'deductions': deductions,
    }
    return render(request, 'payroll_app/view_payslip.html', context)



# void
            # context = {
            #         'b':inp_month,
            #         'l':leap_status,
            #         'r':day_range,
            #         'emp': emp,
            #         'ptest':payslip_test,
            #         }
            # return render(request, 'payroll_app/test.html', context)