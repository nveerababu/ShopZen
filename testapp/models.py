from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('all', 'All Shirts'),
        ('formal', 'Formal Blazers'),
        ('cotton', 'Cotton T-Shirts'),
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Kids', 'Kids'),
        ('Mobiles', 'Mobiles'),
        ('Laptops', 'Laptops'),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='linen')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_path = models.CharField(max_length=255, blank=True, null=True,
                                  help_text="Static image path (e.g., images/img1.png)")
    stock = models.PositiveIntegerField(default=10)          # NEW: how many are left

    def __str__(self):
        return f"{self.name} ({self.category})"

    @property
    def is_sold_out(self):                                    # NEW
        return self.stock == 0



class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    total = models.DecimalField(max_digits=12, decimal_places=2)

    # Checkout customer details
    full_name = models.CharField(max_length=150, default='')
    mobile = models.CharField(max_length=15, default='')
    pincode = models.CharField(max_length=6, default='')
    address = models.TextField(default='')
    payment_method = models.CharField(max_length=20, default='COD')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - Rs.{self.total}"


# NEW: one row per product inside an order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=150)           # saved copy, survives product deletion
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
