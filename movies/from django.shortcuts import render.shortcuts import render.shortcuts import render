from django.shortcuts import render
from .models import Review

def top_comments(request):
    comments = Review.objects.select_related('user', 'movie').order_by('-date')[:20]  # Top 20 recent comments
    return render(request, 'movies/top_comments.html', {'comments': comments})