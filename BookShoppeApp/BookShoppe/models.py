from django.db import models
from django.contrib.auth.models import User
import datetime
import os

def getFileName(request, filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename = "%s%s"%(now_time, filename)
    return os.path.join('uploads/', new_filename)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to=getFileName, null=True, blank=True)
    trending = models.BooleanField(default=False,help_text="0-default,1-Trending")
    quantity = models.IntegerField(null=False,blank=False)

    def __str__(self):
        return self.title
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    book_qty = models.IntegerField(default=False,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return self.book_qty * self.book.price
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.TextField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
