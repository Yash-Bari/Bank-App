from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Account, Loan, CreditCard, Investment, RetirementPlan

admin.site.register(User, UserAdmin)
admin.site.register(Account)
admin.site.register(Loan)
admin.site.register(CreditCard)
admin.site.register(Investment)
admin.site.register(RetirementPlan)
