import random
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='%(app_label)s_%(class)s_set',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='%(app_label)s_%(class)s_set',
    )
    role = models.CharField(max_length=30, choices=[('customer', 'Customer'), ('teller', 'Bank Teller'), ('loan_officer', 'Loan Officer'), ('credit_card_manager', 'Credit Card Manager'), ('financial_advisor', 'Financial Advisor'),('admin','Admin')], default='customer')

# Customer model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)

    def __str__(self):
        return self.name

def generate_account_number():
    """Generate a unique 12-digit account number."""
    while True:
        account_number = str(uuid.uuid4().int)[:12]
        if not Account.objects.filter(account_number=account_number).exists():
            return account_number 

def generate_card_number():
    """Generate a unique 16-digit card number."""
    while True:
        card_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
        if not CreditCard.objects.filter(card_number=card_number).exists():
            return card_number

def generate_cvv():
    """Generate a 3-digit CVV number."""
    return ''.join([str(random.randint(0, 9)) for _ in range(3)])

# Account model
class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True, editable=False, default=generate_account_number)
    account_type = models.CharField(max_length=30, choices=[('checking', 'Checking'), ('savings', 'Savings')])
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.account_type} - {self.account_number}'

# Transaction model
class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')])
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.transaction_type} of {self.amount} on {self.created_at}'

# Loan model
class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=30, choices=[('personal', 'Personal'), ('auto', 'Auto'), ('mortgage', 'Mortgage')])
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.loan_type} loan of {self.amount}'

# Repayment model
class Repayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    repayment_date = models.DateTimeField()

    def __str__(self):
        return f'Repayment of {self.amount} on {self.repayment_date}'

# CreditCard model
class CreditCard(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16, unique=True, editable=False, default=generate_card_number)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2)
    card_type = models.CharField(max_length=30, choices=[('standard', 'Standard'), ('reward', 'Reward')])
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('active', 'Active'), ('rejected', 'Rejected')], default='pending')
    cvv = models.CharField(max_length=3, editable=False, default=generate_cvv)

    def __str__(self):
        return f'{self.card_type} card - {self.card_number}'

# CreditCardTransaction model
class CreditCardTransaction(models.Model):
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=[('purchase', 'Purchase'), ('payment', 'Payment')])
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.transaction_type} of {self.amount} on {self.created_at}'

# Investment model
class Investment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    investment_type = models.CharField(max_length=30, choices=[('stocks', 'Stocks'), ('bonds', 'Bonds'), ('mutual_funds', 'Mutual Funds')])
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    return_rate = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.investment_type} investment of {self.amount}'

# RetirementPlan model
class RetirementPlan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=30, choices=[('ira', 'IRA'), ('401k', '401(k)')])
    contribution = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.plan_type} plan with contribution {self.contribution}'
