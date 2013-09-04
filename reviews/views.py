from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils import timezone
from django.views import generic
import re

from reviews.models import Comic, Reviewer, Review, ComicTag

#################################  LIST VIEWS  #############################################

class ReviewIndexView(generic.ListView):
    def get_queryset(self):
        return Review.objects.order_by('-pub_date')[:10]

class ComicIndexView(generic.ListView):
    def get_queryset(self):
        return Comic.objects.extra( select={'lower_name': 'lower(name)'}).order_by('lower_name')

class ReviewerIndexView(generic.ListView):
    def get_queryset(self):
        return Reviewer.objects.extra( select={'lower_name': 'lower(name)'}).order_by('lower_name')

def filtercomicsbytag(request, tag=""):
    comic_list = Comic.objects.all()
    return render(request, 'reviews/comicsbytag.html', {'comic_list':comic_list, 'search_tag':tag})

#################################  DETAIL VIEWS  #############################################

class ComicDetailView(generic.DetailView):
    model = Comic

class ReviewerDetailView(generic.DetailView):
    model = Reviewer

class ReviewDetailView(generic.DetailView):
    model = Review

#################################  REVIEW MANIP (ALL REQUIRE AUTH) #############################################

def writereview(request, comic_id, rating=0, review_text="Enter Review here...", write_edit='Write', error_message=None):
    comic = get_object_or_404(Comic, pk=comic_id)
    return render(request, 'reviews/writereview.html', {'write_edit'   : write_edit,  
                                                        'comic'        : comic, 
                                                        'review_text'  : review_text,
                                                        'rating'       : rating,
                                                        'error_message': error_message,})

def editreview(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return writereview(request, review.comic.id, review.stars, review.review_text, write_edit='Edit')

def savereview(request, comic_id, write_edit):
    try:
        comic = get_object_or_404(Comic, pk=comic_id)
        reviewer = get_object_or_404(Reviewer, user=request.user) if (request.user and request.user.is_active) else None
        review, created = Review.objects.get_or_create(reviewer=reviewer, comic=comic, defaults={'pub_date': timezone.now()})
        (review.review_text, review.stars) = [request.POST[i] for i in ('review_text', 'rating')]
        review.pub_date = timezone.now() # update timestamps for edits as well as creation
        review.save()
        return HttpResponseRedirect(reverse('comicdetail', args=(comic.id,)))
    except (KeyError):
        return writereview(request, comic_id, write_edit=write_edit, error_message="Malformed Request; try again")
    except (Reviewer.DoesNotExist):
        return writereview(request, comic_id, rating, review_text, write_edit, "Invalid User or Password")

def deletereview(request, review_id, error_message=None):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/deletereview.html', {'review'        : review, 
                                                         'error_message' : error_message,})

def confirmdeletereview(request, review_id):
    try:
        review = get_object_or_404(Review, pk=review_id)
        reviewer = get_object_or_404(Reviewer, user=request.user) if (request.user and request.user.is_active) else None
        if reviewer != review.reviewer:
            return deletereview(request, review_id, "You can only delete your own reviews")
        review.delete()
        return HttpResponseRedirect(reverse('reviewerdetail', args=(reviewer.id,)))
    except (Reviewer.DoesNotExist):
        return deletereview(request, review_id, "Invalid User or Password")

#################################  COMIC MANIP (ALL REQUIRE AUTH)  #############################################

def addcomic(request, comic_id=0, 
             comic_name="Comic Name", comic_url="URL to FIRST STRIP of Comic", 
             comic_mpaa_rating=Comic.RATING_UNRATED, comic_tag_string="",
             add_edit="Add New", error_message=None):
    return render(request, 'reviews/addcomic.html', {'add_edit'            : add_edit,
                                                     'comic_id'            : comic_id,
                                                     'comic_name'          : comic_name,
                                                     'comic_url'           : comic_url,
                                                     'comic_mpaa_rating'   : comic_mpaa_rating,
                                                     'comic_tag_string'    : comic_tag_string,
                                                     'mpaa_rating_choices' : Comic.mpaa_choices(),
                                                     'error_message'       : error_message,});

def editcomic(request, comic_id):
    comic = get_object_or_404(Comic, pk=comic_id)
    return addcomic(request, comic_id, comic.name, comic.url, comic.mpaa_rating, comic.tag_string(), add_edit="Edit")

def tagsfromstring(tag_string):
    tag_string = tag_string.lower()
    tag_string = re.sub(',',' ', tag_string)
    tag_string = re.sub('[^a-zA-Z- ,]','-', tag_string)
    s = set(tag_string.split(" "))
    if '' in s:   s.remove('')
    if None in s: s.remove(None)
    return s

def savecomic(request, comic_id, add_edit):
    try:
        reviewer = get_object_or_404(Reviewer, user=request.user) if (request.user and request.user.is_active) else None
        comic = Comic() if int(comic_id)==0 else get_object_or_404(Comic, pk=comic_id)
        (comic.name, comic.url, comic.mpaa_rating) = [request.POST[i] for i in ('comic_name', 'comic_url', 'mpaa_rating')]
        comic.save()

        comic.comictag_set.all().delete()
        for tag in tagsfromstring(request.POST['tag_string']):
            ComicTag(comic=comic, tag_text=tag).save()

        return HttpResponseRedirect(reverse('comicsindex'))
    except (KeyError):
        return addcomic(request, add_edit=add_edit, error_message="Malformed Request; try again");
    except (Reviewer.DoesNotExist):
        return addcomic(request, comic_name, comic_url, "Invalid User or Password")

def deletecomic(request, comic_id, error_message=None):
    comic = get_object_or_404(Comic, pk=comic_id)
    return render(request, 'reviews/deletecomic.html', {'comic'        : comic, 
                                                        'error_message' : error_message,})

def confirmdeletecomic(request, comic_id):
    try:
        get_object_or_404(Comic, pk=comic_id).delete()
        return HttpResponseRedirect(reverse('comicsindex'))
    except (Reviewer.DoesNotExist):
        return deletecomic(request, comic_id, "Invalid User or Password")

