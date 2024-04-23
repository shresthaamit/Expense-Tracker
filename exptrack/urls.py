from django.urls import path
from django.contrib.auth import views as auth_views
from .import views
urlpatterns = [
    path('', views.loginpage,name='login'),
    path('register',views.registerpage, name='register'),
    path('logout',views.logoutpage, name='logout'),
    path('home',views.home, name='home'),
    path('profile', views.profilewallet,name='profile'),
    path('incomeform', views.incomeform,name="incomeform"),
    path('editincome/<int:id>', views.editIncome, name='editincome'),
    path('deleteincome/<int:id>', views.deleteIncome, name='deleteincome'),
    path('expenseform', views.expensesform,name="expenseform"),
    path('editexpense/<int:id>/',views.editExpenses,name='editexpenses'),
    path('deleteexpenses/<int:id>/', views.deleteExpenses, name='deleteexpenses'),
    path('record/', views.showrecord, name='showrecord'),
    path('allhistory/', views.allhistory, name= 'allhistory'),
    path('generate-pdf/', views.generatepdf, name='generatepdf'),
    path('yearrecord', views.yearly_summary,name='yearrecord'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]