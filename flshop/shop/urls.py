# shop/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # теперь главная страница рендерится как home.html
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('order/create/', views.order_create, name='order_create'),
    path('logout/', LogoutView.as_view(template_name='shop/logout.html'), name='logout'),
]


# urlpatterns = [
#     path('', views.product_list, name='product_list'),
#     path('product/<int:pk>/', views.product_detail, name='product_detail'),
#     path('cart/', views.cart_detail, name='cart_detail'),
#     path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
#     path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
#     path('order/create/', views.order_create, name='order_create'),
# ]
