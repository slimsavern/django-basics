from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Product
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. This is Slim's app There.")

def products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'myapp/index.html', context)

#Class based view for above products view

class ProductListView(ListView):
    model = Product
    template_name = 'myapp/index.html'
    context_object_name = 'products'
    ordering = ['-name']


def product_detail(request, id):
    product = Product.objects.get(id=id)
    context = {'product': product}
    return render(request, 'myapp/product_detail.html', context)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'myapp/product_detail.html'
    context_object_name = 'product'
    ordering = ['-name']

@login_required(login_url='/users/login')
def add_product(request):
    if request.method == 'POST': 
        name = request.POST['name']
        price = request.POST['price']
        desc = request.POST['desc']
        image = request.FILES['upload']
        seller_name = request.user
        Product.objects.create(name=name, price=price, desc=desc, image=image,seller_name=seller_name)
        return HttpResponse("Product added successfully")
    return render(request, 'myapp/addproduct.html')

#class based view for creating a product
class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'price', 'desc', 'image','seller_name']
    #template_name = 'myapp/addproduct.html'
    success_url = '/myapp/products/'

def update_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.desc = request.POST['desc']
        product.image = request.FILES['upload']
        product.save()
        return redirect('/myapp/products/')
    
    context = {'product': product}
    return render(request, 'myapp/updateproduct.html', context)

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'price', 'desc', 'image','seller_name']
    #template_name = 'myapp/updateproduct.html'
    #success_url = '/myapp/products/'
    #template_name = 'myapp/updateproduct.html'
    template_name_suffix: str = '_update_form'
    success_url = '/myapp/products/'
    

def delete_product(request, id):
    product = Product.objects.get(id=id)
    context={'product': product}
    
    if request.method == 'POST':
        product.delete()
        return redirect('/myapp/products/')
    return render(request, 'myapp/deleteproduct.html', context)

class ProductDeleteView(DeleteView):
    model = Product
    #template_name = 'myapp/deleteproduct.html'
    template_name_suffix: str = '_confirm_delete'
    success_url = '/myapp/products/'

def my_listings(request):
    products = Product.objects.filter(seller_name=request.user)
    context = {'products': products}
    return render(request, 'myapp/mylistings.html', context)
# def index(request):