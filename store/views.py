from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Customer, Product, Category, Order, OrderItem, Payment, CustomUser
from .forms import CustomerForm, ProductForm, OrderForm, OrderItemFormSet, PaymentForm, OrderStatusForm

@login_required
def home(request):
    # Dashboard data for the home page
    recent_orders = Order.objects.order_by('-order_date')[:5]
    customer_count = Customer.objects.count()
    product_count = Product.objects.count()
    order_count = Order.objects.count()
    context = {
        'recent_orders': recent_orders,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'store/home.html', context)

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'store/customer_list.html'
    context_object_name = 'customers'

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'store/customer_form.html'
    success_url = reverse_lazy('customer_list')

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'store/customer_form.html'
    success_url = reverse_lazy('customer_list')

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'store/customer_confirm_delete.html'
    success_url = reverse_lazy('customer_list')

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')
    template_name = 'store/product_confirm_delete.html'

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'store/order_list.html'
    context_object_name = 'orders'

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'store/order_form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderItemFormSet(self.request.POST)
            context['order_form'] = self.get_form()  # Ensure form is added as 'order_form'
        else:
            context['formset'] = OrderItemFormSet()
            context['order_form'] = self.get_form()  # Ensure form is added as 'order_form'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            total_amount = sum(item.quantity * item.unit_price for item in self.object.items.all())
            self.object.total_amount = total_amount
            self.object.save()
            return redirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))

class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'store/order_form.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = OrderItemFormSet(self.request.POST)
            context['order_form'] = self.get_form()  # Add the form as 'order_form'
        else:
            context['formset'] = OrderItemFormSet()
            context['order_form'] = self.get_form()  # Add the form as 'order_form'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            # Save the order
            self.object = form.save()
            # Save order items and calculate total_amount
            formset.instance = self.object
            formset.save()
            # Calculate and update total_amount
            total_amount = sum(item.quantity * item.unit_price for item in self.object.items.all())
            self.object.total_amount = total_amount
            self.object.save()
            return redirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))

@login_required
def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'store/order_update_status.html', {'form': form, 'order': order})

class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'store/payment_form.html'

    def form_valid(self, form):
        order = get_object_or_404(Order, pk=self.kwargs['order_id'])
        form.instance.order = order
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('order_list')

