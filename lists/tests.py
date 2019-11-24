from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest

# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolve_to_home_page(self):
        found = resolve('/')
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        html = response.content.decode('utf-8')
        
        self.assertTrue(html.startswith('<html>'))
        self.assertTrue(html.strip().endswith('</html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTemplateUsed(response, 'home.html')