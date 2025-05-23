from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True, db_index=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            ('can_view_sensitive_data', 'Maxfiy ma’lumotlarni ko‘rish'),
        ]

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Qabul qilindi'),
        ('processing', 'Tayyorlanmoqda'),
        ('delivered', 'Yetkazildi'),
        ('canceled', 'Bekor qilindi'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_address = models.TextField(blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    delivery_status = models.CharField(max_length=20, choices=[
        ('pending', 'Kutilmoqda'),
        ('shipped', 'Jo‘natildi'),
        ('delivered', 'Yetkazildi'),
    ], default='pending')

    def save(self, *args, **kwargs):
        # Buyurtma summasini avtomatik hisoblash
        if self.pk:
            items = self.items.all()
            self.total_amount = sum(item.quantity * item.unit_price for item in items)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.customer.name}"

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Buyurtma qilinganda mahsulot narxini saqlash
        if not self.unit_price:
            self.unit_price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    class Meta:
        verbose_name = "Buyurtma elementi"
        verbose_name_plural = "Buyurtma elementlari"

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Naqd'),
        ('card', 'Karta'),
        ('transfer', 'Bank o‘tkazmasi'),
    ]
    STATUS_CHOICES = [
        ('paid', 'To‘langan'),
        ('partial', 'Qisman to‘langan'),
        ('pending', 'Kutilmoqda'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"To‘lov #{self.id} - Buyurtma #{self.order.id}"

    class Meta:
        verbose_name = "To‘lov"
        verbose_name_plural = "To‘lovlar"

class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('in', 'Qabul qilindi'),
        ('out', 'Sotildi'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="transactions")
    quantity = models.IntegerField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Inventar qoldig‘ini yangilash
        if self.transaction_type == 'in':
            self.product.stock += self.quantity
        elif self.transaction_type == 'out':
            self.product.stock -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.transaction_type} ({self.quantity})"

    class Meta:
        verbose_name = "Inventar harakati"
        verbose_name_plural = "Inventar harakatlari"


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)