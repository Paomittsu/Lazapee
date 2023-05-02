from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.employees, name="employees"),
    path('create_employee', views.create_employee, name="create_employee"),
    path('overtime/<int:pk>/', views.overtime, name="overtime"),
    path('delete_employee/<int:pk>/', views.delete_employee, name="delete_employee"),
    # path('test/<int:pk>', views.test, name="test"),
]
