from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ibcomics.views.home', name='home'),
    # url(r'^ibcomics/', include('ibcomics.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^reviews/', include('reviews.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
