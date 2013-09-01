from django.conf.urls import patterns, url

from reviews import views

urlpatterns = patterns('',

#################################  LISTS  #############################################
    # ex: /reviews/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /comics/
    url(r'^comics$', views.ComicIndexView.as_view(), name='comicsindex'),
    # ex: /reviewers/
    url(r'^reviewers$', views.ReviewerIndexView.as_view(), name='reviewersindex'),

#################################  DETAILS  #############################################
    # ex: /reviews/5/
    url(r'^(?P<pk>\d+)/$', views.ReviewDetailView.as_view(), name='detail'),
    # ex: /reviews/comic/5/
    url(r'^comic/(?P<pk>\d+)/$', views.ComicDetailView.as_view(), name='comicdetail'),
    # ex: /reviews/reviewer/5/
    url(r'^reviewer/(?P<pk>\d+)/$', views.ReviewerDetailView.as_view(), name='reviewerdetail'), 

#################################  REVIEW MANIP  #############################################
    # ex: /reviews/writereview/5/
    url(r'^writereview/(?P<comic_id>\d+)/$', views.writereview, name='writereview'),
    # ex: /reviews/editreview/5/
    url(r'^editreview/(?P<review_id>\d+)/$', views.editreview, name='editreview'),
    # ex: /reviews/savereview/5/Write
    url(r'^savereview/(?P<comic_id>\d+)/(?P<write_edit>[a-zA-Z]+)/$', views.savereview, name='savereview'),
    # ex: /reviews/deletereview/5/
    url(r'^deletereview/(?P<review_id>\d+)/$', views.deletereview, name='deletereview'),
    # ex: /reviews/confirmdeletereview/5/
    url(r'^confirmdeletereview/(?P<review_id>\d+)/$', views.confirmdeletereview, name='confirmdeletereview'),

#################################  COMIC MANIP  #############################################
    # ex: /reviews/addcomic/
    url(r'^addcomic/$', views.addcomic, name='addcomic'),
    # ex: /reviews/editcomic/3
    url(r'^editcomic/(?P<comic_id>\d+)/$', views.editcomic, name='editcomic'),
    # ex: /reviews/savecomic/
    url(r'^savecomic/(?P<comic_id>\d+)/(?P<add_edit>[a-zA-Z ]+)/$', views.savecomic, name='savecomic'),
    # ex: /reviews/deletecomic/3
    url(r'^deletecomic/(?P<comic_id>\d+)/$', views.deletecomic, name='deletecomic'),
    # ex: /reviews/confirmdeletecomic/5/
    url(r'^confirmdeletecomic/(?P<comic_id>\d+)/$', views.confirmdeletecomic, name='confirmdeletecomic'),
    
)
