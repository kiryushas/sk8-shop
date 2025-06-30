from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('hoodie', 'Hoodie'),
        ('pants', 'Pants'),
        ('shoes', 'Shoes'),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    
    # Картинка товара (загружается в папку product_images/)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"
