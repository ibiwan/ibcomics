from django.conf.urls import patterns, url

from reviews import views

urlpatterns = patterns('',
    # ex: /reviews/5/
    url(r'^(?P<review_id>\d+)/$', views.detail, name='detail'),
    # ex: /reviews/writereview/5/
    url(r'^writereview/(?P<comic_id>\d+)/$', views.writereview, name='writereview'),
    # ex: /reviews/editreview/5/
    url(r'^editreview/(?P<review_id>\d+)/$', views.editreview, name='editreview'),
    # ex: /reviews/savereview/5/
    url(r'^savereview/(?P<comic_id>\d+)/$', views.savereview, name='savereview'),
    # ex: /reviews/savereview/5/
    url(r'^deletereview/(?P<review_id>\d+)/$', views.deletereview, name='deletereview'),
    # ex: /reviews/savereview/5/
    url(r'^confirmdeletereview/(?P<review_id>\d+)/$', views.confirmdeletereview, name='confirmdeletereview'),
    # ex: /reviews/addcomic/
    url(r'^addcomic/$', views.addcomic, name='addcomic'),
    # ex: /reviews/savecomic/
    url(r'^savecomic/$', views.savecomic, name='savecomic'),

    # ex: /reviews/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /reviews/
    url(r'^comics$', views.ComicIndexView.as_view(), name='comicsindex'),
    # ex: /reviews/comic/5/
    url(r'^comic/(?P<pk>\d+)/$', views.ComicDetailView.as_view(), name='comicdetail'),
    # ex: /reviews/reviewer/5/
    url(r'^reviewer/(?P<pk>\d+)/$', views.ReviewerDetailView.as_view(), name='reviewerdetail'), 
)
