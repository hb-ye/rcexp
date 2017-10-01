from django.conf.urls import patterns, include, url
from django.contrib import admin

#from mysite.views import index, health
from mysite import views ###<<<-------

admin.autodiscover() ###<<<-------

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
 
 ###------->>>
    # url(r'^$', index),
    # url(r'^health$', health),
    # url(r'^admin/', include(admin.site.urls)),
	
	url(r'^$', views.mainpage),
    url(r'^new_exp/$', views.mainpage),
    url(r'^RCE/(\d{4})/$', views.route_choice_exp_admin),
    url(r'^RCE/(\d{4})/results$', views.publish_results),
    # (r'^RCE/(\d{4})/user/$', views.route_choice_exp_user),
    url(r'^RCE/(\d{4})/user/(\d{0,4})', views.route_choice_exp_user),
    url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static/'}), 
    # url(r'^RCE/$', 'mysite.views.mainpage'),
    # url(r'^RCE/(\d{1,4})/$', 'mysite.views.add_user'),
    # url(r'^openshift/', include('openshift.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
###<<<------
]
