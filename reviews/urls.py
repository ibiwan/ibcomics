from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from reviews import views

urlpatterns = patterns('',

#################################  LOGIN/LOGOUT  #############################################

    #ex: /login/
    url(r'^login$', login_required(views.ReviewerIndexView.as_view()), name='loginreviewerindex'),
    #login handler
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    #ex: /logout/
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout_view'),

#################################  LISTS  #############################################
    # ex: /
    url(r'^$', views.ReviewIndexView.as_view(), name='index'),
    # ex: /comics/
    url(r'^comics$', views.ComicIndexView.as_view(), name='comicsindex'),
    # ex: /comicsandtags/
    url(r'^comicsandtags$', views.filtercomicsbytag, name='comicsandtags'),
    # ex: /comicswithtag/27/
    url(r'^comicswithtag/(?P<tag>[a-zA-Z-]+)/$', views.filtercomicsbytag, name='comicswithtag'),
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
    url(r'^writereview/(?P<comic_id>\d+)/$', login_required(views.writereview), name='writereview'),
    # ex: /reviews/editreview/5/
    url(r'^editreview/(?P<review_id>\d+)/$', login_required(views.editreview), name='editreview'),
    # ex: /reviews/savereview/5/Write
    url(r'^savereview/(?P<comic_id>\d+)/(?P<write_edit>[a-zA-Z]+)/$', login_required(views.savereview), name='savereview'),
    # ex: /reviews/deletereview/5/
    url(r'^deletereview/(?P<review_id>\d+)/$', login_required(views.deletereview), name='deletereview'),
    # ex: /reviews/confirmdeletereview/5/
    url(r'^confirmdeletereview/(?P<review_id>\d+)/$', login_required(views.confirmdeletereview), name='confirmdeletereview'),

#################################  COMIC MANIP  #############################################
    # ex: /reviews/addcomic/
    url(r'^addcomic/$', login_required(views.addcomic), name='addcomic'),
    # ex: /reviews/editcomic/3
    url(r'^editcomic/(?P<comic_id>\d+)/$', login_required(views.editcomic), name='editcomic'),
    # ex: /reviews/savecomic/
    url(r'^savecomic/(?P<comic_id>\d+)/(?P<add_edit>[a-zA-Z ]+)/$', login_required(views.savecomic), name='savecomic'),
    # ex: /reviews/deletecomic/3
    url(r'^deletecomic/(?P<comic_id>\d+)/$', login_required(views.deletecomic), name='deletecomic'),
    # ex: /reviews/confirmdeletecomic/5/
    url(r'^confirmdeletecomic/(?P<comic_id>\d+)/$', login_required(views.confirmdeletecomic), name='confirmdeletecomic'),
    
)
