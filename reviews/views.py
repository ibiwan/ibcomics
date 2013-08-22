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

class ComicDetailView(generic.DetailView):
    model = Comic
    template_name = 'reviews/comicdetail.html'

class ReviewerDetailView(generic.DetailView):
    model = Reviewer
    template_name = 'reviews/reviewerdetail.html'

def detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/detail.html', {'review': review})

def writereview(request, comic_id):
    comic = get_object_or_404(Comic, pk=comic_id)
    reviewers = get_list_or_404(Reviewer)
    return render(request, 'reviews/writereview.html', {'reviewers':reviewers, 'comic':comic})

def savereview(request, comic_id):
    comic = get_object_or_404(Comic, pk=comic_id)
    try:
        reviewer_id = request.POST['reviewer']
        reviewer = Reviewer.objects.get(pk=reviewer_id)
        password = request.POST['password']
        user = authenticate(username=reviewer.user.username, password=password)
        if user is None:
            raise PermissionDenied('password incorrect')
    except (KeyError, Reviewer.DoesNotExist):
        reviewers = get_list_or_404(Reviewer)
        # Redisplay the review form.
        return render(request, 'reviews/writereview.html', {
            'comic': comic,
            'reviewers': reviewers,
            'error_message': "You didn't select a reviewer.",})
    else:
        review_text = request.POST['review_text']
        review = Review(reviewer=reviewer, comic=comic, review_text=review_text, stars=5, pub_date=timezone.now())
        review.save()
        return HttpResponseRedirect(reverse('comicdetail', args=(comic.id,)))


