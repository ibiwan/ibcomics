from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied

from reviews.models import Comic, Reviewer, Review

#################################  LISTS  #############################################

class IndexView(generic.ListView):
    template_name = 'reviews/index.html'
    context_object_name = 'latest_review_list'
    def get_queryset(self):
        return Review.objects.order_by('-pub_date')[:5]

class ComicIndexView(generic.ListView):
    template_name = 'reviews/comicsindex.html'
    context_object_name = 'all_comics_list'
    def get_queryset(self):
        return Comic.objects.order_by('name')

class ReviewerIndexView(generic.ListView):
    template_name = 'reviews/reviewersindex.html'
    context_object_name = 'all_reviewers_list'
    def get_queryset(self):
        return Reviewer.objects.order_by('name')

#################################  DETAILS  #############################################

class ComicDetailView(generic.DetailView):
    model = Comic
    template_name = 'reviews/comicdetail.html'

class ReviewerDetailView(generic.DetailView):
    model = Reviewer
    template_name = 'reviews/reviewerdetail.html'

class ReviewDetailView(generic.DetailView):
    model = Review
    template_name = 'reviews/detail.html'

#################################  HELPERS  #############################################

def getAndValidateReviewerByUsername(username, password):
    user = authenticate(username=username, password=password)
    reviewer = Reviewer.objects.get(user=user)
    return reviewer if user else None

#################################  REVIEW MANIP  #############################################

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
        review_text = request.POST['review_text']
        rating = request.POST['rating']
        reviewer = getAndValidateReviewerByUsername(request.POST['username'], 
                                                    request.POST['password'])
        r, created = Review.objects.get_or_create(reviewer=reviewer, comic=comic)
        r.review_text = review_text; r.stars = rating; r.pub_date = timezone.now()
        r.save()
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
        reviewer = getAndValidateReviewerByUsername(request.POST['username'], 
                                                    request.POST['password'])
        if reviewer != review.reviewer:
            return deletereview(request, review_id, "You can only delete your own reviews")
        review.delete()
        return HttpResponseRedirect(reverse('reviewerdetail', args=(reviewer.id,)))
    except (KeyError):
        return deletereview(request, review_id, error_message="Malformed Request; try again")
    except (Reviewer.DoesNotExist):
        return deletereview(request, review_id, "Invalid User or Password")

#################################  COMIC MANIP  #############################################

def addcomic(request, comic_id=0, comic_name="Comic Name", comic_url="URL to FIRST STRIP of Comic", comic_mpaa_rating=Comic.RATING_UNRATED, 
             add_edit="Add New", error_message=None):
    mpaa_rating_choices = Comic.mpaa_choices()
    return render(request, 'reviews/addcomic.html', {'add_edit'            : add_edit,
                                                     'comic_id'            : comic_id,
                                                     'comic_name'          : comic_name,
                                                     'comic_url'           : comic_url,
                                                     'comic_mpaa_rating'   : comic_mpaa_rating,
                                                     'mpaa_rating_choices' : mpaa_rating_choices,
                                                     'error_message'       : error_message,});

def editcomic(request, comic_id):
    comic = get_object_or_404(Comic, pk=comic_id)
    return addcomic(request, comic_id, comic.name, comic.url, comic.mpaa_rating, add_edit="Edit")

def savecomic(request, comic_id, add_edit):
    try:
        comic_name = request.POST['comic_name']
        comic_url = request.POST['comic_url']
        comic_mpaa_rating = request.POST['mpaa_rating']
        reviewer = getAndValidateReviewerByUsername(request.POST['username'],
                                                    request.POST['password'])
        if comic_id > 0:
            c = get_object_or_404(Comic, pk=comic_id)
        else:
            c = Comic()
        c.name=comic_name; c.url = comic_url; c.mpaa_rating = comic_mpaa_rating
        c.save()
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
        comic = get_object_or_404(Comic, pk=comic_id)
        reviewer = getAndValidateReviewerByUsername(request.POST['username'], 
                                                    request.POST['password'])
        comic.delete()
        return HttpResponseRedirect(reverse('comicsindex'))
    except (KeyError):
        return deletecomic(request, comic_id, error_message="Malformed Request; try again")
    except (Reviewer.DoesNotExist):
        return deletecomic(request, comic_id, "Invalid User or Password")

