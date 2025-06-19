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

    def __str__(self):
        return self.name