from decimal import Decimal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import (
    Product,
    Store,
    SellerProfile,
    CustomerProfile,
    CartItem,
    Order,
    OrderItem,
)


def home(request):
    products = Product.objects.all().order_by('-created_at')

    return render(
        request,
        'home.html',
        {
            'products': products,
        }
    )


def stores(request):
    stores = Store.objects.all()

    return render(
        request,
        'stores.html',
        {
            'stores': stores,
        }
    )


def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)

    products = store.products.all().order_by('-created_at')

    return render(
        request,
        'store_detail.html',
        {
            'store': store,
            'products': products,
        }
    )


@login_required
def customer_panel(request):
    customer = get_object_or_404(
        CustomerProfile,
        user=request.user
    )

    orders = customer.orders.all().order_by('-date')

    return render(
        request,
        'customer_panel.html',
        {
            'customer': customer,
            'orders': orders,
        }
    )


@login_required
def cart(request):
    customer = get_object_or_404(
        CustomerProfile,
        user=request.user
    )

    cart_items = CartItem.objects.filter(
        customer=customer
    ).select_related('product')

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'total': total,
        }
    )


@login_required
def payment(request):
    customer = get_object_or_404(
        CustomerProfile,
        user=request.user
    )

    if request.method == 'POST':

        amount = request.POST.get('amount')

        try:
            amount = Decimal(amount)

            if amount <= 0:
                raise ValueError

        except (ValueError, TypeError, ArithmeticError):

            return render(
                request,
                'payment.html',
                {
                    'customer': customer,
                    'error': 'Please enter a valid amount.'
                }
            )

        customer.balance += amount
        customer.save()

        return redirect('customer_panel')

    return render(
        request,
        'payment.html',
        {
            'customer': customer,
        }
    )


@login_required
def order_history(request):
    customer = get_object_or_404(
        CustomerProfile,
        user=request.user
    )

    orders = customer.orders.all().order_by('-date')

    return render(
        request,
        'order_history.html',
        {
            'customer': customer,
            'orders': orders,
        }
    )


def logout_view(request):
    logout(request)

    return redirect('home')


def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        return render(
            request,
            'registration/login.html',
            {
                'error': 'Invalid username or password.'
            }
        )

    return render(
        request,
        'registration/login.html'
    )


def signup(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        phone = request.POST.get('phone')
        role = request.POST.get('role')


        if password != password2:

            return render(
                request,
                'registration/signup.html',
                {
                    'error': 'Passwords do not match.'
                }
            )


        if User.objects.filter(username=username).exists():

            return render(
                request,
                'registration/signup.html',
                {
                    'error': 'This username already exists.'
                }
            )


        if role not in ['customer', 'seller']:

            return render(
                request,
                'registration/signup.html',
                {
                    'error': 'Please select a valid role.'
                }
            )


        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )


        if role == 'customer':

            CustomerProfile.objects.create(
                user=user,
                phone=phone
            )


        elif role == 'seller':

            SellerProfile.objects.create(
                user=user
            )


        login(request, user)

        return redirect('home')


    return render(
        request,
        'registration/signup.html'
    )


@login_required
def seller_panel(request):

    seller = get_object_or_404(
        SellerProfile,
        user=request.user
    )

    stores = Store.objects.filter(
        owner=seller
    )


    # Total number of products
    # across all seller stores

    total_products = Product.objects.filter(
        store__owner=seller
    ).count()


    return render(
        request,
        'seller_panel.html',
        {
            'stores': stores,
            'total_products': total_products,
        }
    )


@login_required
def create_store(request):

    seller_profile = get_object_or_404(
        SellerProfile,
        user=request.user
    )


    if request.method == 'POST':

        name = request.POST.get('name')
        description = request.POST.get('description')


        Store.objects.create(
            name=name,
            description=description,
            owner=seller_profile
        )


        return redirect('seller_panel')


    return render(
        request,
        'create_store.html'
    )


@login_required
def add_product(request, store_id):

    store = get_object_or_404(
        Store,
        id=store_id
    )


    if request.user != store.owner.user:

        return redirect(
            'store_detail',
            store_id=store.id
        )


    if request.method == 'POST':

        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')


        Product.objects.create(
            name=name,
            price=price,
            description=description,
            image=image,
            store=store
        )


        return redirect(
            'store_detail',
            store_id=store.id
        )


    return render(
        request,
        'add_product.html',
        {
            'store': store,
        }
    )


@login_required
def manage_store(request, store_id):

    store = get_object_or_404(
        Store,
        id=store_id
    )


    if request.user != store.owner.user:

        return redirect(
            'seller_panel'
        )


    products = store.products.all().order_by(
        '-created_at'
    )


    return render(
        request,
        'manage_store.html',
        {
            'store': store,
            'products': products,
        }
    )


@login_required
def edit_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )


    if request.user != product.store.owner.user:

        return redirect(
            'seller_panel'
        )


    if request.method == 'POST':

        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')


        product.name = name
        product.price = price
        product.description = description


        if image:

            product.image = image


        product.save()


        return redirect(
            'manage_store',
            store_id=product.store.id
        )


    return render(
        request,
        'edit_product.html',
        {
            'product': product,
        }
    )


@login_required
def delete_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )


    if request.user != product.store.owner.user:

        return redirect(
            'seller_panel'
        )


    store_id = product.store.id


    if request.method == 'POST':

        product.delete()


    return redirect(
        'manage_store',
        store_id=store_id
    )


@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )


    customer = get_object_or_404(
        CustomerProfile,
        user=request.user
    )


    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        customer=customer
    )


    if not created:

        cart_item.quantity += 1

        cart_item.save()


    return redirect('cart')


@login_required
def increase_cart_item(request, item_id):

    customer = get_object_or_404(
        CustomerProfile,
        user=request.user
    )


    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        customer=customer
    )


    cart_item.quantity += 1

    cart_item.save()


    return redirect('cart')


@login_required
def decrease_cart_item(request, item_id):

    customer = get_object_or_404(
        CustomerProfile,
        user=request.user
    )


    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        customer=customer
    )


    if cart_item.quantity > 1:

        cart_item.quantity -= 1

        cart_item.save()

    else:

        cart_item.delete()


    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):

    customer = get_object_or_404(
        CustomerProfile,
        user=request.user
    )


    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        customer=customer
    )


    cart_item.delete()


    return redirect('cart')


@login_required
def checkout(request):

    customer = get_object_or_404(
        CustomerProfile,
        user=request.user
    )


    cart_items = CartItem.objects.filter(
        customer=customer
    ).select_related(
        'product',
        'product__store'
    )


    if not cart_items.exists():

        return redirect('cart')


    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )


    if customer.balance < total:

        return render(
            request,
            'cart.html',
            {
                'cart_items': cart_items,
                'total': total,
                'error': 'Insufficient balance.'
            }
        )


    order = Order.objects.create(
        customer=customer,
        total_amount=total
    )


    for item in cart_items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )


        store = item.product.store

        store.balance += (
            item.product.price * item.quantity
        )

        store.save()


    customer.balance -= total

    customer.save()


    cart_items.delete()


    return redirect(
        'order_history'
    )