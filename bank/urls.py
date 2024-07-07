from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Authentication URLs
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('teller_dashboard/', views.teller_dashboard, name='teller_dashboard'),
    path('loan_officer_dashboard/', views.loan_officer_dashboard, name='loan_officer_dashboard'),
    path('credit_card_manager_dashboard/', views.credit_card_manager_dashboard, name='credit_card_manager_dashboard'),
    path('financial_advisor_dashboard/', views.financial_advisor_dashboard, name='financial_advisor_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Customer management URLs
    path('create_customer/', views.create_customer, name='create_customer'),
    path('edit_customer/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('delete_customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),
    path('create_account/<int:user_id>/', views.create_account, name='create_account'),

    # Admin user management URLs
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),

    # Customer application URLs
    path('apply_loan/', views.apply_loan, name='apply_loan'),
    path('apply_credit_card/', views.apply_credit_card, name='apply_credit_card'),
    path('apply_investment/', views.apply_investment, name='apply_investment'),
    path('apply_retirement_plan/', views.apply_retirement_plan, name='apply_retirement_plan'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/new/', views.create_transaction, name='create_transaction'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)