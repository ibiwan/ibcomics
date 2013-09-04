from django.contrib import admin
from reviews.models import Comic, Reviewer, Review, ComicTag

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class TagInline(admin.TabularInline):
    model = ComicTag
    extra = 3

class ReviewAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Select', {'fields': ['comic', 'reviewer']}), 
        ('Enter', {'fields': ['pub_date', 'stars', 'review_text']})
    ]
    list_display = ('reviewer', 'stars', 'comic')
    list_filter = ('pub_date',)
    search_fields = ('review_text', 'comic__name', 'reviewer__name')
    date_hierarchy = 'pub_date'

class ComicAdmin(admin.ModelAdmin):
    inlines = [TagInline, ReviewInline]
    list_display = ('name', 'url')

class ReviewerAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
    list_display = ('name',)

admin.site.register(Comic, ComicAdmin)
admin.site.register(Reviewer, ReviewerAdmin)
admin.site.register(Review, ReviewAdmin)
