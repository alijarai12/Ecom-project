from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from app.forms import LoginForm

urlpatterns = [
    path('', views.index, name="index"),
    #path('login/', views.user_login, name="login"),
    path('accounts/register/', views.register, name="register"),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account/login.html', authentication_form=LoginForm), name="login"),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name="logout"),

    path('accounts/profile/', views.profile, name="profile"),

    path('activate/<uidb64>/<token>', views.activate, name="activate"),



    path('productdetail/<int:pk>', views.productdetail, name='productdetail'),
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('orders/', views.orders, name="orders"),
    path('caty/', views.caty, name="caty"),

    path('plus-cart/<int:cart_id>/', views.plus_cart, name="plus-cart"),
    path('minus-cart/<int:cart_id>/', views.minus_cart, name="minus-cart"),
    path('remove-cart/<int:cart_id>/', views.remove_cart, name="remove-cart"),


]