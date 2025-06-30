from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('card', 'Card'),
        ('crypto', 'Crypto'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'id': 'payment-method'})
    )

    # Для оплаты картой
    card_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Card number'}))
    card_expiry = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    card_cvv = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'CVV'}))

    # Для оплаты криптой
    crypto_network = forms.ChoiceField(
        choices=[
            ('trc20', 'TRC20'),
            ('bnb', 'BNB'),
            ('eth', 'Ethereum'),
        ],
        required=False,
        widget=forms.Select()
    )
    crypto_address = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Your wallet address'}))

    class Meta:
        model = Order
        fields = ['full_name', 'address', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }