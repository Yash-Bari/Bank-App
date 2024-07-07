from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User, Customer, Account, Loan, CreditCard, Investment, RetirementPlan, generate_account_number, Transaction
from .forms import UserForm, CustomerForm, AccountForm, LoanForm, CreditCardForm, InvestmentForm, RetirementPlanForm, LoginForm, EditUserForm
from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib import messages
from decimal import Decimal


# Check if user is a specific role
def check_role(role):
    def inner(user):
        return user.role == role or user.role == 'admin'
    return inner

# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('dashboard')
            else:
                return HttpResponse('Invalid login credentials')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard view based on user role
@login_required
def dashboard(request):
    if request.user.role == 'customer':
        return redirect('customer_dashboard')
    elif request.user.role == 'teller':
        return redirect('teller_dashboard')
    elif request.user.role == 'loan_officer':
        return redirect('loan_officer_dashboard')
    elif request.user.role == 'credit_card_manager':
        return redirect('credit_card_manager_dashboard')
    elif request.user.role == 'financial_advisor':
        return redirect('financial_advisor_dashboard')
    elif request.user.role == 'admin':
        return redirect('admin_dashboard')
    else:
        return HttpResponse('Unauthorized', status=401)

# Customer dashboard
@login_required
@user_passes_test(check_role('customer'))
def customer_dashboard(request):
    customer = get_object_or_404(Customer, user=request.user)
    accounts = Account.objects.filter(customer=customer)
    loans = Loan.objects.filter(customer=customer)
    credit_cards = CreditCard.objects.filter(customer=customer)
    investments = Investment.objects.filter(customer=customer)
    retirement_plans = RetirementPlan.objects.filter(customer=customer)
    return render(request, 'customer_dashboard.html', {
        'customer': customer,
        'accounts': accounts,
        'loans': loans,
        'credit_cards': credit_cards,
        'investments': investments,
        'retirement_plans': retirement_plans
    })

@login_required
@user_passes_test(check_role('customer'))
def transaction_list(request):
    accounts = Account.objects.filter(customer=request.user.customer)
    transactions = Transaction.objects.filter(account__in=accounts)
    return render(request, 'transaction_list.html', {'transactions': transactions})

@login_required
@user_passes_test(check_role('customer'))
def create_transaction(request):
    if request.method == 'POST':
        account_id = request.POST.get('account')
        transaction_type = request.POST.get('transaction_type')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        try:
            amount = Decimal(amount)
        except ValueError:
            messages.error(request, 'Invalid amount.')
            return redirect('create_transaction')

        account = Account.objects.get(id=account_id, customer=request.user.customer)

        if transaction_type == 'withdrawal' and account.balance < amount:
            messages.error(request, 'Insufficient funds. Your current balance is {}'.format(account.balance))
            return redirect('create_transaction')

        if transaction_type == 'deposit':
            account.balance += amount
        elif transaction_type == 'withdrawal':
            account.balance -= amount

        account.save()

        Transaction.objects.create(
            account=account,
            transaction_type=transaction_type,
            amount=amount,
            description=description
        )

        messages.success(request, 'Transaction successful.')
        return redirect('transaction_list')

    accounts = Account.objects.filter(customer=request.user.customer)
    return render(request, 'create_transaction.html', {'accounts': accounts})


# Bank Teller dashboard
@login_required
@user_passes_test(check_role('teller'))
def teller_dashboard(request):
    accounts = Account.objects.all()
    customers = Customer.objects.all()  # Add this to get all customers
    return render(request, 'teller_dashboard.html', {'accounts': accounts, 'customers': customers})

@login_required
@user_passes_test(check_role('teller'))
def create_customer(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, request.FILES)
        if customer_form.is_valid():
            customer = customer_form.save(commit=False)
            username = customer.email.split('@')[0]
            password = generate_password()

            user = User.objects.create_user(
                username=username,
                email=customer.email,
                password=password
            )
            customer.user = user
            customer.save()

            # Send credentials to customer via email
            subject = 'Your Bank Account Credentials'
            message = f'Your account has been created successfully. Your username is {username} and your password is {password}.'
            from_email = 'yashbari99@gmail.com'
            to_email = customer.email
            send_mail(subject, message, from_email, [to_email])

            return redirect('create_account', user_id=user.id)  # Redirect to create_account view with user ID
    else:
        customer_form = CustomerForm()

    return render(request, 'create_customer.html', {'customer_form': customer_form})

# Function to generate a random password
def generate_password():
    return get_random_string(length=12, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()')

@login_required
@user_passes_test(check_role('teller'))
def create_account(request, user_id):
    user = get_object_or_404(User, id=user_id)
    customer = get_object_or_404(Customer, user=user)  # Get Customer associated with the User
    
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account = account_form.save(commit=False)
            account.customer = customer
            account.save()
            return redirect('teller_dashboard')  # Redirect to Teller Dashboard
    else:
        account_form = AccountForm()
    
    account_number = generate_account_number()

    return render(request, 'create_account.html', {'account_form': account_form, 'customer': customer, 'account_number': account_number})

@login_required
@user_passes_test(check_role('teller'))
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, request.FILES, instance=customer)
        if customer_form.is_valid():
            customer_form.save()
            return redirect('teller_dashboard')  # Redirect to Teller Dashboard after saving
    else:
        customer_form = CustomerForm(instance=customer)

    return render(request, 'edit_customer.html', {'customer_form': customer_form, 'customer': customer})

@login_required
@user_passes_test(check_role('teller'))
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.delete()
    return redirect('teller_dashboard')  # Redirect to Teller Dashboard after deleting

# Loan Officer dashboard
@login_required
@user_passes_test(check_role('loan_officer'))
def loan_officer_dashboard(request):
    loans = Loan.objects.all()
    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')
        action = request.POST.get('action')
        loan = Loan.objects.get(id=loan_id)
        if action == 'approve':
            loan.status = 'approved'
        elif action == 'reject':
            loan.status = 'rejected'
        loan.save()
        return redirect('loan_officer_dashboard')
    return render(request, 'loan_officer_dashboard.html', {'loans': loans})

# Credit Card Manager dashboard
@login_required
@user_passes_test(check_role('credit_card_manager'))
def credit_card_manager_dashboard(request):
    credit_cards = CreditCard.objects.all()
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        action = request.POST.get('action')
        credit_card = CreditCard.objects.get(id=card_id)
        if action == 'approve':
            credit_card.status = 'active'
        elif action == 'reject':
            credit_card.status = 'rejected'
        credit_card.save()
        return redirect('credit_card_manager_dashboard')
    return render(request, 'credit_card_manager_dashboard.html', {'credit_cards': credit_cards})

# Financial Advisor dashboard
@login_required
@user_passes_test(check_role('financial_advisor'))
def financial_advisor_dashboard(request):
    investments = Investment.objects.all()
    return render(request, 'financial_advisor_dashboard.html', {'investments': investments})

# Admin dashboard
@login_required
@user_passes_test(check_role('admin'))
def admin_dashboard(request):
    users = User.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users})

# Add user view
@login_required
@user_passes_test(check_role('admin'))
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.username = form.cleaned_data['email'].split('@')[0]  # Generate username from email
            user.save()
            return redirect('admin_dashboard')  # Redirect to a success page
    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})

# Edit user view
@login_required
@user_passes_test(check_role('admin'))
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if 'email' in form.changed_data:
                user.username = form.cleaned_data['email'].split('@')[0]
            user.save()
            return redirect('admin_dashboard')
    else:
        form = UserForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})

# Delete user view
@login_required
@user_passes_test(check_role('admin'))
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_dashboard')

# Customer application views
@login_required
@user_passes_test(check_role('customer'))
def apply_loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.customer = get_object_or_404(Customer, user=request.user)
            loan.save()
            return redirect('customer_dashboard')
    else:
        form = LoanForm()
    return render(request, 'apply_loan.html', {'form': form})

@login_required
@user_passes_test(check_role('customer'))
def apply_credit_card(request):
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        if form.is_valid():
            credit_card = form.save(commit=False)
            credit_card.customer = get_object_or_404(Customer, user=request.user)
            credit_card.save()
            return redirect('customer_dashboard')
    else:
        form = CreditCardForm()
    return render(request, 'apply_credit_card.html', {'form': form})

@login_required
@user_passes_test(check_role('customer'))
def apply_investment(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.customer = get_object_or_404(Customer, user=request.user)
            investment.save()
            return redirect('customer_dashboard')
    else:
        form = InvestmentForm()
    return render(request, 'apply_investment.html', {'form': form})

@login_required
@user_passes_test(check_role('customer'))
def apply_retirement_plan(request):
    if request.method == 'POST':
        form = RetirementPlanForm(request.POST)
        if form.is_valid():
            retirement_plan = form.save(commit=False)
            retirement_plan.customer = get_object_or_404(Customer, user=request.user)
            retirement_plan.save()
            return redirect('customer_dashboard')
    else:
        form = RetirementPlanForm()
    return render(request, 'apply_retirement_plan.html', {'form': form})
