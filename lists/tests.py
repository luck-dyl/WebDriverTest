from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest

# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolve_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
    
    def test_home_page_returns_correct_html(self):
        req = HttpRequest()
        res = home_page(req)
        html = res.content.decode('utf-8')
        print(repr(html))
        self.assertTrue(html.startswith('<html>'))
        self.assertTrue(html.strip().endswith('</html>'))
        self.assertIn('<title>To-Do lists</title>', html)