from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item, Message
from .forms import MessageForm

def item_list(request):
    items = Item.objects.filter(is_available=True).order_by('-created_at')
    return render(request, 'listings/item_list.html', {'items': items})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = MessageForm()
    return render(request, 'listings/item_detail.html', {'item': item, 'form': form})

@login_required
def send_message(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # Prevent sellers from messaging themselves
    if request.user == item.seller:
        messages.error(request, "You can't message yourself about your own listing.")
        return redirect('item-detail', pk=pk)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.item = item
            message.sender = request.user
            message.receiver = item.seller
            message.save()
            messages.success(request, 'Message sent! The seller will get back to you.')
            return redirect('item-detail', pk=pk)

    return redirect('item-detail', pk=pk)

@login_required
def inbox(request):
    received = Message.objects.filter(receiver=request.user).order_by('-created_at')
    sent = Message.objects.filter(sender=request.user).order_by('-created_at')
    
    # Mark all received messages as read when inbox is opened
    received.filter(is_read=False).update(is_read=True)
    
    return render(request, 'listings/inbox.html', {'received': received, 'sent': sent})