from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Movie, Review, MoviePetition
from .forms import PetitionForm


def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {
        'title': 'Movies',
        'movies': movies
    }
    return render(request, 'movies/index.html', {'template_data': template_data})


def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)

    template_data = {
        'title': movie.name,
        'movie': movie,
        'reviews': reviews
    }
    return render(request, 'movies/show.html', {'template_data': template_data})


@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.content = request.POST['comment']   # use content
        review.movie = movie
        review.author = request.user              # use author
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)


@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.author:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {
            'title': 'Edit Review',
            'review': review
        }
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review.content = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)


@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, author=request.user)
    review.delete()
    return redirect('movies.show', id=id)


def top_comments(request):
    top_comments = Review.objects.select_related('author', 'movie').order_by('-created_at')[:20]
    return render(request, 'movies/top_comments.html', {'top_comments': top_comments})


def likes(request):
    return render(request, 'movies/likes.html')


# 🔹 Petition logic inside filler
def filler(request):
    petitions = MoviePetition.objects.all().order_by("-created_at")

    # Only allow logged-in users to POST petitions
    if request.method == "POST":
        if request.user.is_authenticated:
            form = PetitionForm(request.POST)
            if form.is_valid():
                petition = form.save(commit=False)
                petition.created_by = request.user
                petition.save()
                return redirect("filler")
        else:
            return redirect("login")  # redirect anonymous users to login
    else:
        form = PetitionForm()

    return render(request, 'movies/filler.html', {
        "form": form,
        "petitions": petitions,
    })


@login_required
def vote_petition(request, petition_id):
    petition = get_object_or_404(MoviePetition, id=petition_id)

    # toggle vote (if user already voted, remove it; otherwise add it)
    if request.user in petition.votes.all():
        petition.votes.remove(request.user)
    else:
        petition.votes.add(request.user)

    return redirect("filler")
