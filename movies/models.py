from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')

    def __str__(self):
        return str(self.id) + ' - ' + self.name

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=0)  # 1–5 stars, for example
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:30]}"
