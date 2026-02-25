from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Item
from .models import Item, Message

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'is_available', 'created_at']
    list_filter = ['category', 'is_available']      
    
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'item', 'is_read', 'created_at']
    list_filter = ['is_read']
    
    