# forms.py

from django import forms
from .models import User, Customer, Account, Loan, CreditCard, Investment, RetirementPlan

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'role', 'password']

class EditUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'role']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'dob', 'address', 'phone_number', 'profile_picture']  # Ensure 'birthday' is included

    # Ensure the 'birthday' field is displayed as a date input
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # Use 'date' input type for date selection
        label='Date of Birth'
    )
        
class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type', 'balance']

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['loan_type', 'amount', 'interest_rate', 'term_months']

class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['credit_limit', 'card_type']

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['investment_type', 'amount', 'return_rate']

class RetirementPlanForm(forms.ModelForm):
    class Meta:
        model = RetirementPlan
        fields = ['plan_type', 'contribution']
