from django.urls import path

from .views import (
    home,
    stores,
    store_detail,
    customer_panel,
    cart,
    payment,
    order_history,
    logout_view,
    login_view,
    signup,
    seller_panel,
    create_store,
    add_product,
    manage_store,
    edit_product,
    delete_product,
    add_to_cart,
    increase_cart_item,
    decrease_cart_item,
    remove_from_cart,
    checkout,
)


urlpatterns = [

    path(
        '',
        home,
        name='home'
    ),

    path(
        'stores/',
        stores,
        name='stores'
    ),

    path(
        'stores/<int:store_id>/',
        store_detail,
        name='store_detail'
    ),


    # Customer

    path(
        'customer/',
        customer_panel,
        name='customer_panel'
    ),

    path(
        'cart/',
        cart,
        name='cart'
    ),

    path(
        'payment/',
        payment,
        name='payment'
    ),

    path(
        'orders/',
        order_history,
        name='order_history'
    ),


    # Authentication

    path(
        'logout/',
        logout_view,
        name='logout'
    ),

    path(
        'login/',
        login_view,
        name='login'
    ),

    path(
        'signup/',
        signup,
        name='signup'
    ),


    # Seller

    path(
        'seller/',
        seller_panel,
        name='seller_panel'
    ),

    path(
        'seller/create-store/',
        create_store,
        name='create_store'
    ),

    path(
        'seller/store/<int:store_id>/add-product/',
        add_product,
        name='add_product'
    ),

    path(
        'seller/store/<int:store_id>/manage/',
        manage_store,
        name='manage_store'
    ),

    path(
        'seller/product/<int:product_id>/edit/',
        edit_product,
        name='edit_product'
    ),

    path(
        'seller/product/<int:product_id>/delete/',
        delete_product,
        name='delete_product'
    ),


    # Cart

    path(
        'cart/add/<int:product_id>/',
        add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/increase/<int:item_id>/',
        increase_cart_item,
        name='increase_cart_item'
    ),

    path(
        'cart/decrease/<int:item_id>/',
        decrease_cart_item,
        name='decrease_cart_item'
    ),

    path(
        'cart/remove/<int:item_id>/',
        remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'checkout/',
        checkout,
        name='checkout'
    ),
]