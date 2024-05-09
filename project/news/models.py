from django.db import models
from django.contrib.auth.models import User
from .Pos import CATEGORY_POST, NEWS
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def up_rating(self):
        postRating = self.post_set.aggregate(
            post_rating=Sum('post__rating'))  # сбор данных поля, к которому применяется функция
        pRat = 0
        pRat += postRating.get('rating')

        comRating = self.authorUser.comment_set.aggregate(
            comment_rating=Sum('comment__rating'))  # замена цикла for
        cRat = 0
        cRat += comRating.get('rating')

        self._author_rating = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category_type = models.CharField(max_length=2, choices=CATEGORY_POST, default=NEWS)
    time_in = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    titl = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:128] + '...'

    #def __str__(self):
    #    return f'{self.author.title()}: {self.text[:20]}'


class PostCategory(models.Model):
    _post = models.ForeignKey(Post, on_delete=models.CASCADE)
    _category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    comUser = models.ForeignKey(User, on_delete=models.CASCADE)
    comText = models.CharField(max_length=256, null=False)
    comTime = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
