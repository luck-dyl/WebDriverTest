from django.test import TestCase

# Create your tests here.
class SmokeTest(TestCase):
    def test_add(self):
       self.assertEqual(1, 3 + 8)

