from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.views import generic
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied

from reviews.models import Comic, Reviewer, Review

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

class ComicDetailView(generic.DetailView):
    model = Comic
    template_name = 'reviews/comicdetail.html'

class ReviewerDetailView(generic.DetailView):
    model = Reviewer
    template_name = 'reviews/reviewerdetail.html'

def detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    indices = range(1,6)
    return render(request, 'reviews/detail.html', {'review': review, 'indices': indices})

########################################################################################

def getAndValidateReviewer(reviewer_id, password):
    reviewer = Reviewer.objects.get(pk=reviewer_id)
    user = authenticate(username=reviewer.user.username, password=password)
    return reviewer if user else None

########################################################################################

def writereview(request, comic_id, review_text="Enter Review here...", error_message=None):
    comic = get_object_or_404(Comic, pk=comic_id)
    reviewers = get_list_or_404(Reviewer)
    return render(request, 'reviews/writereview.html', {'reviewers':reviewers, 
                                                            'comic':comic, 
                                                      'review_text':review_text,
                                                    'error_message':error_message,})

def savereview(request, comic_id):
    try:
        comic = get_object_or_404(Comic, pk=comic_id)
        review_text = request.POST['review_text']
        reviewer = getAndValidateReviewer(request.POST['reviewer'], request.POST['password'])
        if reviewer is None:
            return writereview(request, comic_id, review_text, "Invalid User or Password")
    except (KeyError):
        return writereview(request, comic_id, review_text, "Malformed Request; try again")
    else:
        Review(reviewer=reviewer, comic=comic, review_text=review_text, stars=5, pub_date=timezone.now()).save()
        return HttpResponseRedirect(reverse('comicdetail', args=(comic.id,)))

def deletereview(request, review_id, error_message=None):
    review = get_object_or_404(Review, pk=review_id)
    reviewers = get_list_or_404(Reviewer)
    return render(request, 'reviews/deletereview.html', {'reviewers':reviewers, 
                                                            'review':review, 
                                                    'error_message':error_message,})

def confirmdeletereview(request, review_id):
    try:
        review  = get_object_or_404(Review, pk=review_id)
        reviewer = getAndValidateReviewer(request.POST['reviewer'], request.POST['password'])
        if reviewer is None:
            return deletereview(request, review_id, "Invalid User or Password")
        if reviewer != review.reviewer:
            return deletereview(request, review_id, "You can only delete your own reviews")
    except (KeyError):
        return deletereview(request, review_id, "Malformed Request; try again")
    else:
        review.delete()
        return HttpResponseRedirect(reverse('reviewerdetail', args=(reviewer.id,)))

########################################################################################

def addcomic(request, comic_name="Comic Name", comic_url="URL to FIRST STRIP of Comic", error_message=None):
    reviewers = get_list_or_404(Reviewer)
    return render(request, 'reviews/addcomic.html', {'comic_name': comic_name,
                                                      'comic_url': comic_url,
                                                      'reviewers': reviewers,
                                                  'error_message': error_message,});

def savecomic(request):
    try:
        comic_name = request.POST['comic_name']
        comic_url = request.POST['comic_url']
        reviewer = getAndValidateReviewer(request.POST['reviewer'], request.POST['password'])
        if reviewer is None:
            return addcomic(request, comic_name, comic_url, "Invalid User or  Password");
    except (KeyError):
        return addcomic(request, comic_name, comic_url, "Malformed Request; try again");
    else:
        Comic(name=comic_name, url=comic_url).save()
        return HttpResponseRedirect(reverse('comicsindex'))


