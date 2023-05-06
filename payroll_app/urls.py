from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.employees, name="employees"),
    path('create_employee', views.create_employee, name="create_employee"),
    path('overtime/<int:pk>/', views.overtime, name="overtime"),
    path('delete_employee/<int:pk>/', views.delete_employee, name="delete_employee"),
    path('update_employee/<int:pk>/', views.update_employee, name="update_employee"),
    path('view_payslips', views.view_payslips, name="view_payslips"),
    # path('test/<int:pk>', views.test, name="test"),
]
