from django.test import TestCase
from store.forms import CustomerForm

class FormTests(TestCase):
    def test_customer_form_valid(self):
        """To‘g‘ri ma’lumotlar bilan forma sinovi"""
        form_data = {
            'name': 'Ali Valiyev',
            'phone': '+998901234567',
            'email': 'ali@example.com',
            'address': 'Toshkent'
        }
        form = CustomerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_customer_form_invalid_phone(self):
        """Noto‘g‘ri telefon raqami bilan forma sinovi"""
        form_data = {
            'name': 'Ali Valiyev',
            'phone': 'invalid_phone',
            'email': 'ali@example.com',
            'address': 'Toshkent'
        }
        form = CustomerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)