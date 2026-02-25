from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_list, name='item-list'),
    path('item/<int:pk>/', views.item_detail, name='item-detail'),
    path('item/<int:pk>/message/', views.send_message, name='send-message'),
    path('inbox/', views.inbox, name='inbox'),
]