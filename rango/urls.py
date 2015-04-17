from django.conf.urls import patterns, url

from rango import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^about/', views.about, name='about'),
	url(r'^add_category/$', views.add_category, name='add_category'),
	# ?P for parameter
	# [\w\-]+ Will find any Char followed by a - before a /
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='page'),

	url(r'^restricted/$', views.restricted, name='restricted'),
	url(r'^search/$', views.search, name='search'),
	url(r'^add_profile/', views.register_profile, name="add_profile"),
	url(r'^goto/$', views.track_url, name='goto')
	)