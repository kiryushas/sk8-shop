from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    payment_info = forms.CharField(
        label='Payment Details (Card/Crypto)',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter card number or crypto wallet address'
        })
    )

    class Meta:
        model = Order
        fields = ['full_name', 'address', 'phone', 'payment_info']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shipping address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
        }

    def save(self, commit=True):
        order = super().save(commit=False)
        order.payment_info = self.cleaned_data['payment_info']
        if commit:
            order.save()
        return order
