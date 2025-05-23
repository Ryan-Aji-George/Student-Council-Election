from django.contrib import admin

from .models import Post, Candidate, Vote

class CandidateInline(admin.StackedInline):
    model = Candidate
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [CandidateInline]
    list_display = ('post_title', 'is_house_captain', 'house', 'order')

admin.site.register(Post, PostAdmin)
admin.site.register(Candidate)
admin.site.register(Vote)

admin.site.site_header = "Voting Administration"
admin.site.site_title = "Voting Admin Portal"
admin.site.index_title = "Welcome to Voting Administration"

