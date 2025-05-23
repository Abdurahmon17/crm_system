from rest_framework import serializers
from .models import Category, Customer, Product, Order, OrderItem, Payment

class CategorySerializer(serializers.ModelSerializer):
   class Meta:
       model = Category
       fields = ['id', 'name']

class CustomerSerializer(serializers.ModelSerializer):
   class Meta:
       model = Customer
       fields = ['id', 'name', 'phone', 'email', 'address']

class ProductSerializer(serializers.ModelSerializer):
   category = CategorySerializer(read_only=True)
   category_id = serializers.PrimaryKeyRelatedField(
       queryset=Category.objects.all(), source='category', write_only=True
   )

   class Meta:
       model = Product
       fields = ['id', 'name', 'category', 'category_id', 'price', 'stock', 'description']

class OrderItemSerializer(serializers.ModelSerializer):
   product = ProductSerializer(read_only=True)
   product_id = serializers.PrimaryKeyRelatedField(
       queryset=Product.objects.all(), source='product', write_only=True
   )

   class Meta:
       model = OrderItem
       fields = ['id', 'product', 'product_id', 'quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
   customer = CustomerSerializer(read_only=True)
   customer_id = serializers.PrimaryKeyRelatedField(
       queryset=Customer.objects.all(), source='customer', write_only=True
   )
   items = OrderItemSerializer(many=True, read_only=True)

   class Meta:
       model = Order
       fields = ['id', 'customer', 'customer_id', 'order_date', 'status', 'total_amount',
                 'delivery_address', 'delivery_date', 'delivery_status', 'items']

class PaymentSerializer(serializers.ModelSerializer):
   order = OrderSerializer(read_only=True)
   order_id = serializers.PrimaryKeyRelatedField(
       queryset=Order.objects.all(), source='order', write_only=True
   )

   class Meta:
       model = Payment
       fields = ['id', 'order', 'order_id', 'amount', 'payment_method', 'payment_date', 'status']