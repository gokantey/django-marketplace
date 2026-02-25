from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Item

class ItemModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='seller', password='pass1234')
        self.item = Item.objects.create(
            name='Test Laptop',
            description='A great laptop for testing.',
            price=499.99,
            category='electronics',
            is_available=True,
            seller=self.user
        )

    def test_item_str(self):
        """Item __str__ returns its name"""
        self.assertEqual(str(self.item), 'Test Laptop')

    def test_item_default_availability(self):
        """Items are available by default"""
        self.assertTrue(self.item.is_available)

    def test_item_belongs_to_seller(self):
        """Item is correctly linked to its seller"""
        self.assertEqual(self.item.seller.username, 'seller')


class ItemListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='seller', password='pass1234')
        Item.objects.create(
            name='Phone', description='Nice phone', price=299.99,
            category='electronics', is_available=True, seller=self.user
        )
        Item.objects.create(
            name='Sold Chair', description='Old chair', price=50.00,
            category='furniture', is_available=False, seller=self.user
        )

    def test_list_page_loads(self):
        """Item list page returns 200"""
        response = self.client.get(reverse('item-list'))
        self.assertEqual(response.status_code, 200)

    def test_only_available_items_shown(self):
        """Sold items don't appear on the listing page"""
        response = self.client.get(reverse('item-list'))
        self.assertContains(response, 'Phone')
        self.assertNotContains(response, 'Sold Chair')

    def test_list_uses_correct_template(self):
        """List view uses the right template"""
        response = self.client.get(reverse('item-list'))
        self.assertTemplateUsed(response, 'listings/item_list.html')


class ItemDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='seller', password='pass1234')
        self.item = Item.objects.create(
            name='Vintage Chair',
            description='A beautiful vintage chair.',
            price=120.00,
            category='furniture',
            is_available=True,
            seller=self.user
        )

    def test_detail_page_loads(self):
        """Item detail page returns 200"""
        response = self.client.get(reverse('item-detail', args=[self.item.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detail_shows_item_name(self):
        """Detail page displays the item name"""
        response = self.client.get(reverse('item-detail', args=[self.item.pk]))
        self.assertContains(response, 'Vintage Chair')

    def test_detail_shows_price(self):
        """Detail page displays the price"""
        response = self.client.get(reverse('item-detail', args=[self.item.pk]))
        self.assertContains(response, '120')

    def test_invalid_item_returns_404(self):
        """Requesting a non-existent item returns 404"""
        response = self.client.get(reverse('item-detail', args=[9999]))
        self.assertEqual(response.status_code, 404)