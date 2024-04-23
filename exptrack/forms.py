from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.forms import Form
from .models import Income,Expenses

class CustomUserCreationForm(UserCreationForm):
    # email = forms.EmailField()

    # class Meta(UserCreationForm.Meta):
    #     fields = ['username', 'email', 'password1', 'password2']

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         raise ValidationError("Email already exists")
    #     return email
    username = forms.CharField(min_length=1, max_length=14)
    email = forms.EmailField()
    password1 = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password',widget=forms.PasswordInput)
    
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        newuser  = User.objects.filter(username=username)
        if newuser.count():
            raise ValidationError("User already exists.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        newemail = User.objects.filter(email=email)
        if newemail.count():
            raise ValidationError("Email already exist")
        return email
     
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password doesnot match")
        return password2
    
    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    password = forms.CharField(max_length=65, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    
    class Meta:
        fields = ["email"]
labels = {
"email": ""
}
widgets = {
"test": forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email to"}))
}
       
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email')
    




class IncomeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['user'].required = False
        # if user:
        #     self.fields['user'].queryset = User.objects.filter(username=user.username)

        # self.fields['user'].queryset = User.objects.filter(username=self.initial.get('user'))
    class Meta:
        model = Income
        fields = ['user','profession', 'source_1_name', 'source_1_amount', 'source_2_name', 'source_2_amount', 'source_3_name', 'source_3_amount']
        widgets = {
            'profession': forms.Select(attrs={'class': 'form-select'}),
            'source_1_name': forms.TextInput(attrs={'class': 'form-control'}),
            'source_1_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'source_2_name': forms.TextInput(attrs={'class': 'form-control'}),
            'source_2_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'source_3_name': forms.TextInput(attrs={'class': 'form-control'}),
            'source_3_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
        }
     
class ExpenseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['user'].required = False
    class Meta:
        model = Expenses
        fields =['user', 'source_1_name', 'source_1_amount', 'source_2_name', 'source_2_amount', 'source_3_name', 'source_3_amount']
        widgets = {
                
                'source_1_name': forms.TextInput(attrs={'class': 'form-control'}),
                'source_1_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
                'source_2_name': forms.TextInput(attrs={'class': 'form-control'}),
                'source_2_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
                'source_3_name': forms.TextInput(attrs={'class': 'form-control'}),
                'source_3_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            }
    # name = forms.CharField(label='Full Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # source_1_name = forms.CharField(label='Source 1', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # source_1_amount = forms.DecimalField(label='', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}))
    # source_2_name = forms.CharField(label='Source 2', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # source_2_amount = forms.DecimalField(label='', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}))
    # source_3_name = forms.CharField(label='Source 3', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # source_3_amount = forms.DecimalField(label='', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}))
    