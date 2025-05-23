from django.test import TestCase
from django.core.exceptions import ValidationError
from store.models import Customer, Product, Category, Order, OrderItem

class ModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Erkaklar kiyimi")
        self.customer = Customer.objects.create(
            name="Ali Valiyev",
            phone="+998901234567",
            email="ali@example.com"
        )
        self.product = Product.objects.create(
            name="Ko‘ylak",
            category=self.category,
            price=150000,
            stock=50
        )

    def test_customer_creation(self):
        """Mijoz yaratishni sinash"""
        self.assertEqual(self.customer.name, "Ali Valiyev")
        self.assertEqual(self.customer.phone, "+998901234567")

    def test_product_stock_validation(self):
        """Mahsulot qoldig‘i manfiy bo‘lmasligini sinash"""
        with self.assertRaises(ValidationError):
            product = Product(
                name="Shim",
                category=self.category,
                price=200000,
                stock=-10
            )
            product.full_clean()

    def test_order_total_amount(self):
        """Buyurtma umumiy summasini sinash"""
        order = Order.objects.create(customer=self.customer, status="pending")
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
            unit_price=self.product.price
        )
        order.save()  # Total amount yangilash
        self.assertEqual(order.total_amount, 300000)  # 2 * 150000