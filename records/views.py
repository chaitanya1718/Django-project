from django.shortcuts import render, redirect, get_object_or_404
# # Create your views here.

from .models import Employee, Department, Role, Contact
from .forms import EmployeeForm, ContactForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth.views import LoginView
from django.db.models import Q



# bln to identify user/admin
def is_superuser(user):
    return user.is_superuser



# class to diffrnce btn admin/nomral usr
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return '/adminDashboard'  
        else:
            return '/empDashboard/'   


#admin functions craetion

# func to rander admin page
@login_required
@user_passes_test(is_superuser)
def adminDashboard(request):
    return render(request, 'dashboard.html')


#fnc to view currnt cmpny emplyes
@login_required
@user_passes_test(is_superuser)
def displayEmployees(request):
    employees = (Employee.objects
                 .filter(is_active=True)
                 .select_related('department', 'role', 'contact')
                  .prefetch_related('contact') 
                  )
    query = request.GET.get('q')
    dept_filter = request.GET.get('department')
    role_filter = request.GET.get('role')
    sort_by = request.GET.get('sort')

    if query:
        employees = employees.filter(
            Q(name__icontains=query)
        )

    if dept_filter:
        employees = employees.filter(department__name=dept_filter)

    if role_filter:
        employees = employees.filter(role__name=role_filter)

    if sort_by:
        if sort_by == "joining_date":
            employees = employees.order_by('joining_date')
        elif sort_by == "department":
            employees = employees.order_by('department__name')
        elif sort_by == "role":
            employees = employees.order_by('role__name')


    departments = Department.objects.all()
    roles = Role.objects.all()

    return render(request, 'employee_list.html', {
        'employees': employees,
        'departments': departments,
        'roles': roles,
    })


#func to add emp
@login_required
@user_passes_test(is_superuser)
def addEmployee(request):
    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST)
        contact_form = ContactForm(request.POST)
        user_form = UserCreationForm(request.POST)

        if employee_form.is_valid() and contact_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()

            contact = contact_form.save(commit=False)
            contact.employee = employee
            contact.save()

            return redirect('employee_list')
    else:
        employee_form = EmployeeForm()
        contact_form = ContactForm()
        user_form = UserCreationForm()

    return render(request, 'add_new_employee.html', {
        'employee_form': employee_form,
        'contact_form': contact_form,
        'user_form': user_form
    })


#fnc to delete exiting usr
@login_required
@user_passes_test(is_superuser)
def removeEmployee(request, id):
    employee = get_object_or_404(Employee, id=id)

    employee.is_active = False
    employee.save()

    employee.user.is_active = False
    employee.user.save()

    return redirect('employee_list')

#fnc to add dleted usr
@login_required
@user_passes_test(is_superuser)
def undo_del_employee(request, id):
    employee = get_object_or_404(Employee, id=id)

    employee.is_active = True
    employee.save()

    employee.user.is_active = True
    employee.user.save()

    return redirect('employee_list')





#fnc to viaew past emplyees
@login_required
@user_passes_test(is_superuser)
def pastEmployees(request):
    employees = (Employee.objects
                 .filter(is_active=False)
                 .select_related('department', 'role', 'contact'))
    
    return render(request, 'past_employees.html', {
        'employees': employees
    })



#fnc to register new user/employee
def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        employee_form = EmployeeForm(request.POST)
        contact_form = ContactForm(request.POST)

        if user_form.is_valid() and employee_form.is_valid() and contact_form.is_valid():
            user = user_form.save()
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()

            contact = contact_form.save(commit=False)
            contact.employee = employee
            contact.save()

            login(request, user)
            return redirect('login')
    else:
        user_form = CustomUserCreationForm()
        employee_form = EmployeeForm()
        contact_form = ContactForm()
    
    return render(request, 'register.html', {
        'user_form': user_form,
        'employee_form': employee_form,
        'contact_form': contact_form
    })


@login_required
def userDashboard(request):
    employee = get_object_or_404(Employee, user=request.user)
    contact = get_object_or_404(Contact, employee=employee)

    # Get all employees in the same department (excluding the current user)
    members = Employee.objects.filter(department=employee.department).exclude(id=employee.id)
    
    # Preload contact info and attach to each member
    contact_map = {c.employee.id: c for c in Contact.objects.filter(employee__in=members)}
    for member in members:
        member.contact = contact_map.get(member.id)

    return render(request, 'userDashboard.html', {
        'employee': employee,
        'contact': contact,
        'members': members,
    })