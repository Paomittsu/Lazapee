from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.employees, name="employees"),
    path('create_employee', views.create_employee, name="create_employee"),
    path('overtime/<int:pk>/', views.overtime, name="overtime"),
    path('delete_employee/<int:pk>/', views.delete_employee, name="delete_employee"),
    path('update_employee/<int:pk>/', views.update_employee, name="update_employee"),
    path('payslips', views.payslips, name="payslips"),
    path('payslip_submit', views.payslip_submit, name="payslip_submit"),
    path('view_payslip/<int:pk>', views.view_payslip, name="view_payslip"),
]
