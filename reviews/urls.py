from django.conf.urls import patterns, url

from reviews import views

urlpatterns = patterns('',
    # ex: /reviews/5/
    url(r'^(?P<review_id>\d+)/$', views.detail, name='detail'),
    # ex: /reviews/writereview/5/
    url(r'^writereview/(?P<comic_id>\d+)/$', views.writereview, name='writereview'),
    # ex: /reviews/savereview/5/
    url(r'^savereview/(?P<comic_id>\d+)/$', views.savereview, name='savereview'),

    # ex: /reviews/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /reviews/comic/5/
    url(r'^comic/(?P<pk>\d+)/$', views.ComicDetailView.as_view(), name='comicdetail'),
    # ex: /reviews/reviewer/5/
    url(r'^reviewer/(?P<pk>\d+)/$', views.ReviewerDetailView.as_view(), name='reviewerdetail'), 
)
