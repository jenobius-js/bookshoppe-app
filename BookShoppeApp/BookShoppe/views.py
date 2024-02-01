from django.http import JsonResponse
from django.shortcuts import render,redirect
from BookShoppe.forms import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json
from django.db.models import Q


def index(request):
    books = Book.objects.filter(trending=1)
    return render(request, "BookShoppe/index.html",{"books" : books})

def book_list(request):
    books = Book.objects.all()
    return render(request, "BookShoppe/book_list.html", {"books" : books})

def book_details(request, btitle):
    if(Book.objects.filter(title = btitle)):
        books = Book.objects.filter(title=btitle).first()
        return render(request, "BookShoppe/book_details.html", {"books" : books})
    else:
        messages.error(request,"No Such Book Found")
        return redirect('book_list')
    
def search_books(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        books = Book.objects.filter(Q(title=searched) | Q(author=searched))
        if not books.exists():
            return render(request, "BookShoppe/search_books.html", {"searched": searched})
        else:
            return render(request, "BookShoppe/search_books.html", {"searched": searched, "books": books})
    else:
         return render(request, "BookShoppe/search_books.html")


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully")
    return redirect('/')

def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username = name, password = pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in Successfully")
                return redirect('/')
            else:
                messages.error(request,"Invalid User Name or Password")
        return render(request, "BookShoppe/login.html")

def sign_up(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration Success You can Login Now...!')
            return redirect('/login_page')
    return render(request, "BookShoppe/sign_up.html", {'form': form})


def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.load(request)
            book_qty = data['book_qty']
            book_id = data['bid']
            book_status = Book.objects.get(id=book_id)
            if book_status:
                if Cart.objects.filter(user=request.user.id, book_id=book_id):
                    return JsonResponse({'status': 'Book Already in Cart'}, status=200)
                else:
                    if book_status.quantity >= book_qty:
                        Cart.objects.create(user=request.user, book_id=book_id, book_qty=book_qty)
                        return JsonResponse({'status': 'Book Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Book Stock Not Available'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)


def cart_page(request):
        if request.user.is_authenticated:
            cart=Cart.objects.filter(user=request.user)
            return render(request, "BookShoppe/cart.html", {"cart" : cart})


        else:
            return redirect('/')

def remove_cart(request,cid):
    cartitem = Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")

def checkout(request):
    return render(request, "BookShoppe/checkout.html")

def place_order(request):
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        if not shipping_address:
            messages.error(request, 'Please provide a valid shipping address.')
            return redirect('/checkout')
        else:
            cart_items = Cart.objects.filter(user=request.user)
            total_cost = sum(cart_item.total_cost for cart_item in cart_items)
            order = Order.objects.create(user=request.user, shipping_address=shipping_address, total_cost=total_cost)
            for cart_item in cart_items:
                OrderItem.objects.create(order=order, book=cart_item.book, quantity=cart_item.book_qty, price=cart_item.book.price)
            cart_items.delete()
            return render(request, 'BookShoppe/confirmation.html', {'order': order})
    return redirect('/cart')

