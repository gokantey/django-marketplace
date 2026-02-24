from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Item

def item_list(request):
    items = Item.objects.filter(is_available=True).order_by('-created_at')
    return render(request, 'listings/item_list.html', {'items': items})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'listings/item_detail.html', {'item': item})