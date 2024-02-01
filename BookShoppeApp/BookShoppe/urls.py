from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('book_list/', views.book_list, name='book-list'),
    path('book_list/<str:btitle>', views.book_details, name='book_details'),
    path('cart/', views.cart_page, name='cart'),
    path('remove_cart/<str:cid>', views.remove_cart, name='remove_cart'),
    path('search_books/',views.search_books,name='search_books'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login_page/', views.login_page, name='login_page'),
    path('logout_page/', views.logout_page, name='logout_page'),
    path('addtocart', views.add_to_cart, name='addtocart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
]