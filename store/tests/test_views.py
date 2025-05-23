from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Customer

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='123456')
        self.customer = Customer.objects.create(name="Ali Valiyev", phone="+998901234567")

    def test_customer_list_view_authenticated(self):
        """Autentifikatsiya qilingan foydalanuvchi uchun mijozlar ro‘yxatini sinash"""
        self.client.login(username='testuser', password='123456')
        response = self.client.get(reverse('customer_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ali Valiyev")

    def test_customer_list_view_unauthenticated(self):
        """Autentifikatsiya qilinmagan foydalanuvchi uchun kirishni sinash"""
        response = self.client.get(reverse('customer_list'))
        self.assertEqual(response.status_code, 302)  # Login sahifasiga yo‘naltiradi
        self.assertRedirects(response, '/login/?next=/customers/')

    def test_order_create_view(self):
        """Buyurtma qo‘shishni sinash"""
        self.client.login(username='testuser', password='123456')
        response = self.client.post(reverse('order_create'), {
            'customer': self.customer.id,
            'status': 'pending',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-0-product': '1',
            'form-0-quantity': '2',
        })
        self.assertEqual(response.status_code, 302)  # Muvaffaqiyatli yo‘naltirish
        self.assertEqual(Order.objects.count(), 1)