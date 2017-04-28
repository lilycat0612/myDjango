from django.conf.urls import patterns, url

urlpatterns = patterns('',

	url(r'^(\d+)/$','lists.views.view_list',name='view_list'),#(.+),匹配随后的/之前任意个字符，捕获得到的文本作为参数传入视图,\d只匹配数字
	url(r'^(\d+)/add_item$','lists.views.add_item',name='add_item'),
	url(r'^new$','lists.views.new_list',name='new_list'),
   
)
