from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item, List

# Create your tests here.
class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        
class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        
        first_item = Item()
        first_item.text = "计划买个棉被"
        first_item.list = list_
        first_item.save()    
        
        second_item = Item()
        second_item.text = "计划买个锤子"
        second_item.list = list_
        second_item.save()
        
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "计划买个棉被")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "计划买个锤子")
        self.assertEqual(second_saved_item.list, list_, )
        
class ListViewTest(TestCase):
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)
        
        other_list = List.objects.create()
        Item.objects.create(text="itemy other_list 1", list=other_list)
        Item.objects.create(text="itemy other_list 2", list=other_list)
        
        
        response = self.client.get(f'/lists/{correct_list.id}/')
        
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'itemey other_list 1')
        self.assertNotContains(response, 'itemey other_list 2')
        
    def test_user_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')
        
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context['list'], correct_list)
        
class NewListTest(TestCase):
        
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(f'/lists/{correct_list.id}/add_item', data={'item_text': 'a new list item for an existing list'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        
        self.assertEqual(new_item.text, 'a new list item for an existing list')
        self.assertEqual(new_item.list, correct_list)
        
    def test_redirects_after_to_list_view(self):
        # 验证重定向
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(f'/lists/{correct_list.id}/add_item', data={'item_text': 'a new list item for an existing list'})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
