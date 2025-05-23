from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from store.models import Customer, Category, Product

class APITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='123456')
        self.client.login(username='testuser', password='123456')
        self.category = Category.objects.create(name="Erkaklar kiyimi")
        self.customer = Customer.objects.create(name="Ali Valiyev", phone="+998901234567")
        self.product = Product.objects.create(
            name="Ko‘ylak",
            category=self.category,
            price=150000,
            stock=50
        )

    def test_get_customers(self):
        """Mijozlar ro‘yxatini olishni sinash"""
        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Ali Valiyev")

    def test_create_product_unauthorized(self):
        """Admin bo‘lmagan foydalanuvchi mahsulot qo‘shishni sinash"""
        response = self.client.post('/api/products/', {
            'name': 'Shim',
            'category_id': self.category.id,
            'price': 200000,
            'stock': 30
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product_admin(self):
        """Admin sifatida mahsulot qo‘shishni sinash"""
        admin = User.objects.create_superuser(username='admin', password='admin123')
        self.client.login(username='admin', password='admin123')
        response = self.client.post('/api/products/', {
            'name': 'Shim',
            'category_id': self.category.id,
            'price': 200000,
            'stock': 30
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)