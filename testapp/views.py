from django.shortcuts import render
from django.contrib.auth.decorators import login_required


#about page view
def aboutpage_view(request):
    return render(request, 'about.html')

# conatct page view 
def conatctpage_view(request):
    return render(request,'contactus.html')

#updates page view
def updatespage_view(request):
    return render(request,'updates.html')


from testapp.forms import SignUpForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings


def signupform_view(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()

            # Send welcome email
            send_mail(
                subject="Welcome to ShopZen!",
                message=(
                    f"Hello {user.username},\n\n"
                    "Your ShopZen account has been created successfully.\n"
                    "Thank you for joining us. Happy Shopping!"
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=True,
            )

            return HttpResponseRedirect('/accounts/login/')

    return render(request, 'signup.html', {'form': form})


#logout page view
from django.contrib.auth import logout
from django.shortcuts import redirect
def logout_view(request):
    logout(request)
    return render (request,'logout.html')








def navbar_view(request):
    return render (request, 'navbar.html')

from django.shortcuts import render
from testapp.models import Product
def homepage_view(request):
    selected_category = request.GET.get('category', 'all')

    if selected_category == 'all' or not selected_category:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category=selected_category)

    context = {
        'products': products,
        'selected_category': selected_category,
    }
    return render(request, 'homepage.html', context)



from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from testapp.forms import ProductForm
from testapp.models import Product

#checking of the manager or staff
class ManagerOrStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        return (
            user.is_superuser
            or user.is_staff
            or user.groups.filter(name='Manager').exists()
        )


# 1. Homepage / List View (Public - Evarina chudavachu)
class ProductListView(ListView):
    model = Product
    template_name = 'homepage.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = self.request.GET.get('category', 'all')
        if category == 'all' or not category:
            return Product.objects.all()
        return Product.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_category'] = self.request.GET.get('category', 'all')
        return context


# 2. Add Product (Only Manager or Staff)
class ProductCreateView(ManagerOrStaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('home')


# 3. Update Product (Only Manager or Staff)
class ProductUpdateView(ManagerOrStaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'id'


# 4. Delete Product (Only Manager or Staff)
class ProductDeleteView(ManagerOrStaffRequiredMixin, DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'id'





from django.shortcuts import render
from django.db.models import Q
from .models import Product

def homepage_view(request):
    products = Product.objects.all()

    # Search
    q = request.GET.get('q', '')
    if q:
        products = products.filter(name__icontains=q)

    # Category filter
    category = request.GET.get('category', 'all')
    if category != 'all':
        products = products.filter(category=category)

    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    # Sorting
    sort = request.GET.get('sort')

    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')

    return render(request, 'homepage.html', {
        'products': products,
        'search_query': q,
        'selected_category': category,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'sort_by': sort or '',
    })








from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product


# 1. Add to Cart View
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)

        cart = request.session.get('cart', {})
        p_id = str(product.id)

        cart[p_id] = cart.get(p_id, 0) + 1

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart')


@login_required
def cart_view(request):
    cart = request.session.get('cart', {})

    cart_items = []
    total_price = 0
    invalid_ids = []

    for product_id, quantity in list(cart.items()):
        product = Product.objects.filter(id=product_id).first()

        if product:
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        else:
            invalid_ids.append(product_id)

    if invalid_ids:
        for p_id in invalid_ids:
            cart.pop(p_id, None)
        request.session['cart'] = cart
        request.session.modified = True

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })







@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_items = [{
        'product': product,
        'quantity': 1,
        'subtotal': product.price,
    }]

    if request.method == 'POST':
        checkout_data = {
            'full_name': request.POST.get('full_name', '').strip(),
            'mobile': request.POST.get('mobile', '').strip(),
            'pincode': request.POST.get('pincode', '').strip(),
            'address': request.POST.get('address', '').strip(),
            'payment_method': request.POST.get('payment_method', 'COD'),
        }

        if not all([
            checkout_data['full_name'],
            checkout_data['mobile'],
            checkout_data['pincode'],
            checkout_data['address'],
        ]):
            messages.error(request, 'Please fill all checkout details.')
            return redirect('buy_now', product_id=product.id)

        try:
            create_order(request.user, cart_items, checkout_data)
        except OutOfStock as e:
            messages.error(request, f'Sorry, {e}.')
            return redirect('home')

        messages.success(request, 'Order placed successfully!')
        return redirect('order_success')

    return render(request, 'buy_now.html', {
        'cart_items': cart_items,
        'total_price': product.price,
        'from_cart': False,
    })


@login_required
def checkout_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []

    for product_id, quantity in cart.items():
        product = Product.objects.filter(id=product_id).first()

        if product:
            quantity = int(quantity)
            if quantity > 0:
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': product.price * quantity,
                })

    if not cart_items:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart')

    total_price = sum(
        (item['subtotal'] for item in cart_items),
        start=0
    )

    if request.method == 'POST':
        checkout_data = {
            'full_name': request.POST.get('full_name', '').strip(),
            'mobile': request.POST.get('mobile', '').strip(),
            'pincode': request.POST.get('pincode', '').strip(),
            'address': request.POST.get('address', '').strip(),
            'payment_method': request.POST.get('payment_method', 'COD'),
        }

        if not all([
            checkout_data['full_name'],
            checkout_data['mobile'],
            checkout_data['pincode'],
            checkout_data['address'],
        ]):
            messages.error(request, 'Please fill all checkout details.')
            return redirect('checkout_cart')

        try:
            create_order(request.user, cart_items, checkout_data)
        except OutOfStock as e:
            messages.error(request, f'Sorry, not enough stock: {e}.')
            return redirect('cart')

        request.session['cart'] = {}
        request.session.modified = True

        messages.success(request, 'Order placed successfully!')
        return redirect('order_success')

    return render(request, 'buy_now.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'from_cart': True,
    })


class OutOfStock(Exception):
    pass

# def order_success(request):
#     return render(request, 'order_success.html')


from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render


@login_required
def order_success(request):
    user = request.user
    customer_email = user.email
    email_sent = False

    if not customer_email:
        print(f"WARNING: User '{user.username}' does not have an associated email address.")
    else:
        subject = 'Order Confirmation - ShopZen'
        message = f"""Dear {user.username},

Thank you for shopping with ShopZen.

We are pleased to inform you that your order has been successfully placed.
Our fulfillment team is actively processing your shipment, and you will receive further tracking updates once the package is dispatched.

Order Details:
===========
Status: Confirmed
Store: ShopZen Online Store

If you have any questions or require assistance regarding your order, 
please do not hesitate to contact our customer support team at support@shopzen.com.

Best regards,
The ShopZen Team
"""
        try:
            sent_count = send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[customer_email],
                fail_silently=False,
            )
            if sent_count > 0:
                email_sent = True
                print(f"SUCCESS: Order confirmation email successfully delivered to {customer_email}")
        except Exception as e:
            print(f"EMAIL FAILED ERROR: {e}")

    # Professional flash message
    messages.success(request, "Your order has been confirmed successfully. Thank you for your purchase!")

    
    return render(request, 'order_success.html')

from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.db.models import F, Sum
from django.shortcuts import render

from testapp.models import Order, OrderItem, Product

LOW_STOCK_LIMIT = 5


class OutOfStock(Exception):
    pass


@transaction.atomic
def create_order(user, cart_items, checkout_data=None):
    checkout_data = checkout_data or {}

    total_amount = sum(
        (item['product'].price * int(item['quantity'])
         for item in cart_items),
        start=0
    )

    order = Order.objects.create(
        user=user if user.is_authenticated else None,
        total=total_amount,
        full_name=checkout_data.get('full_name', ''),
        mobile=checkout_data.get('mobile', ''),
        pincode=checkout_data.get('pincode', ''),
        address=checkout_data.get('address', ''),
        payment_method=checkout_data.get('payment_method', 'COD'),
    )

    for item in cart_items:
        product = item['product']
        quantity = int(item['quantity'])

        updated = Product.objects.filter(
            id=product.id,
            stock__gte=quantity
        ).update(stock=F('stock') - quantity)

        if not updated:
            raise OutOfStock(
                f'Insufficient stock for {product.name}'
            )

        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            price=product.price,
            quantity=quantity,
        )

    return order



@staff_member_required
def dashboard_view(request):
    # ---- 1. Inventory Summary ----
    total_products = Product.objects.count()
    sold_out = Product.objects.filter(stock__lte=0).count()
    low_stock = Product.objects.filter(stock__gt=0, stock__lte=LOW_STOCK_LIMIT).count()
    in_stock = Product.objects.filter(stock__gt=LOW_STOCK_LIMIT).count()

    # ---- 2. Business Totals ----
    total_revenue = Order.objects.aggregate(t=Sum('total'))['t'] or 0
    total_orders = Order.objects.count()
    units_sold = OrderItem.objects.aggregate(t=Sum('quantity'))['t'] or 0

    return render(request, 'dashboard.html', {
        # Inventory cards
        'total_products': total_products,
        'in_stock': in_stock,
        'low_stock': low_stock,
        'sold_out': sold_out,
        # Sales cards
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'units_sold': units_sold,
        # Tables / Action items
        'attention_products': Product.objects.filter(stock__lte=LOW_STOCK_LIMIT).order_by('stock'),
        'recent_orders': Order.objects.select_related('user').order_by('-created_at')[:8],
        'low_limit': LOW_STOCK_LIMIT,
    })






