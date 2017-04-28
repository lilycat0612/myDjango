#单元测试结构：1）设置配合 2）执行代码 3）断言判定

from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item,List

# Create your tests here.
class HomePageTest(TestCase):
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func,home_page)
		
	def test_home_page_retruns_crrect_html(self):
		request=HttpRequest()
		response=home_page(request)
		expected_html=render_to_string('home.html')
		self.assertEqual(response.content.decode(),expected_html)
		
		# self.assertTrue(response.content.startswith(b'<html>'))
		# self.assertIn(b'<title>To-do lists</title>',response.content)
		# self.assertTrue(response.content.endswith(b'</html>'))
	

	
	def test_home_page_only_saves_item_when_necessary(self):
		request=HttpRequest()
		home_page(request)
		self.assertEqual(Item.objects.count(),0)
		
		
		
# class ItemModelTest(TestCase):
class ListAndItemModelsTest(TestCase):
	def test_saving_and_retrieving_items(self):
		list_=List()
		list_.save()
		
		first_item=Item()
		first_item.text='The first (ever) list item'
		first_item.list=list_
		first_item.save()
		
		second_item=Item()
		second_item.text='Item the second'
		second_item.list=list_
		second_item.save()
		
		saved_list=List.objects.first()
		self.assertEqual(saved_list,list_)
		
		saved_items=Item.objects.all()
		self.assertEqual(saved_items.count(),2)
		
		first_saved_item=saved_items[0]
		second_saved_item=saved_items[1]
		self.assertEqual(first_saved_item.text,'The first (ever) list item')
		self.assertEqual(first_saved_item.list,list_)
		self.assertEqual(second_saved_item.text,'Item the second')
		self.assertEqual(second_saved_item.list,list_)
		
class ListViewTest(TestCase):
	def test_uses_list_template(self):
		# response=self.client.get('/lists/the-only-list-in-the-world/')
		list_=List.objects.create()
		response=self.client.get('/lists/%d/' % (list_.id,))
		self.assertTemplateUsed(response,'list.html')
	
	# def test_home_page_displays_all_list_items(self):
		# 设置配置
		# Item.objects.create(text='itemey 1')
		# Item.objects.create(text='itemey 2')
		
	# def test_displays_all_item(self):
	
		# list_=List.objects.create()
		# Item.objects.create(text='itemey 1',list=list_)
		# Item.objects.create(text='itemey 2',list=list_)
		
		# 执行代码
		# response=self.client.get('/lists/the-only-list-in-the-world/')
		# 断言
		# self.assertContains(response,'itemey 1')
		# self.assertContains(response,'itemey 2')
	
	def test_displays_only_item_for_that_list(self):
		correct_list=List.objects.create()
		Item.objects.create(text='itemey 1',list=correct_list)
		Item.objects.create(text='itemey 2',list=correct_list)
		other_list=List.objects.create()
		Item.objects.create(text='other list item 1',list=other_list)
		Item.objects.create(text='other list item 2',list=other_list)
		
		response=self.client.get('/lists/%d/' % (correct_list.id,))
		
		self.assertContains(response,'itemey 1')
		self.assertContains(response,'itemey 2')
		self.assertNotContains(response,'other list item 1')
		self.assertNotContains(response,'other list item 2')
	
	def test_passes_correct_list_to_template(self):
		other_list=List.objects.create()
		correct_list=List.objects.create()
		
		response=self.client.get('/lists/%d/' %(correct_list.id,))
		
		self.assertEqual(response.context['list'],correct_list)
		
		
class NewListTest(TestCase):
	def test_saving_a_POST_request(self):
		# 设置配置
		# request=HttpRequest()
		# request.method='POST'
		# request.POST['item_text']='A new list item'
		# 执行代码
		# response=home_page(request)
		self.client.post('/lists/new',data={'item_text':'A new list item'})
		#断言:是否存入正确存入数据库
		self.assertEqual(Item.objects.count(),1)
		new_item=Item.objects.first()
		self.assertEqual(new_item.text,'A new list item')
		
		#断言
		# self.assertIn('A new list item',response.content.decode())
		# exceptd_html=render_to_string('home.html',{'new_item_text':'A new list item'})
		# self.assertEqual(response.content.decode(),exceptd_html)
		
	
	def test_redirects_after_POST(self):
		#设置配置
		# request=HttpRequest()
		# request.method='POST'
		# request.POST['item_text']='A new list item'
		#执行代码
		# response=home_page(request)	
		response=self.client.post('/lists/new',data={'item_text':'A new list item'})
		new_list=List.objects.first()
		#断言
		#self.assertEqual(response.status_code,302)

		# self.assertRedirects(response,'/lists/the-only-list-in-the-world/')
		self.assertRedirects(response,'/lists/%d/' %(new_list.id,))
	
	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list=List.objects.create()
		correct_list=List.objects.create()
		
		self.client.post('/lists/%d/add_item' %(correct_list.id,),data={'item_text':'A new item for an existing list'})
		
		self.assertEqual(Item.objects.count(),1)
		new_item=Item.objects.first()
		self.assertEqual(new_item.text,'A new item for an existing list')
		self.assertEqual(new_item.list,correct_list)
	
	def test_redirects_to_list_view(self):
		other_list=List.objects.create()
		correct_list=List.objects.create()
		
		response=self.client.post('/lists/%d/add_item' %(correct_list.id,),data={'item_text':'A new item for an existing list'})
		
		self.assertRedirects(response,'/lists/%d/' %(correct_list.id,))
	
	