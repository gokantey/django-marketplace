from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

class ProfileAutoCreateTest(TestCase):

    def test_profile_created_on_user_signup(self):
        """A Profile is automatically created when a User is created"""
        user = User.objects.create_user(username='testuser', password='pass1234')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_profile_str(self):
        """Profile __str__ returns the correct string"""
        user = User.objects.create_user(username='testuser', password='pass1234')
        self.assertEqual(str(user.profile), "testuser's Profile")


class RegisterViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_page_loads(self):
        """Register page returns 200"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_user_can_register(self):
        """A new user can register successfully"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 302)  # redirect after success
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_creates_profile(self):
        """Registering a user also creates their profile"""
        self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        user = User.objects.get(username='newuser')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_duplicate_username_fails(self):
        """Registering with an existing username fails"""
        User.objects.create_user(username='taken', password='pass1234')
        response = self.client.post(reverse('register'), {
            'username': 'taken',
            'email': 'other@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 200)  # stays on page, not redirected
        self.assertContains(response, 'already exists')


class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass1234')

    def test_login_page_loads(self):
        """Login page returns 200"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_valid_login_redirects(self):
        """Logging in with correct credentials redirects"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'pass1234',
        })
        self.assertEqual(response.status_code, 302)

    def test_invalid_login_fails(self):
        """Wrong password keeps user on login page"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)


class ProfileViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass1234')

    def test_profile_page_loads(self):
        """Profile page returns 200"""
        response = self.client.get(reverse('profile', args=['testuser']))
        self.assertEqual(response.status_code, 200)

    def test_profile_shows_username(self):
        """Profile page displays the username"""
        response = self.client.get(reverse('profile', args=['testuser']))
        self.assertContains(response, 'testuser')

    def test_nonexistent_profile_returns_404(self):
        """Visiting a profile that doesn't exist returns 404"""
        response = self.client.get(reverse('profile', args=['ghost']))
        self.assertEqual(response.status_code, 404)

    def test_edit_profile_requires_login(self):
        """Edit profile page redirects unauthenticated users"""
        response = self.client.get(reverse('edit-profile'))
        self.assertEqual(response.status_code, 302)