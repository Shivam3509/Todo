from django.shortcuts import render
from .models import Item,Record
# Create your views here.
def Index(request):
    context={}
    data = Item.objects.all()
    context['data'] = data
    if request.method == 'POST':
        quantity = request.POST['quantity']
        product = Item.objects.get(id=request.POST['id'])
        total = product.price * int(quantity)
        Record.objects.create(productname=product,quantity=quantity,price=total)
        context['product'] = product
        context['quantity'] = quantity
        context['price'] = total
    return render(request, 'index.html', context)