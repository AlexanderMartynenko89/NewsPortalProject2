from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default = 0)

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comments_rating = Comment.objects.filter(user=self.user).aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        posts_comment_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Coalesce(Sum('rating'), 0))['pcr']

        print(f'Рейтинг статьи автора - {posts_rating}')
        print(f'Рейтинг всех комментариев автора - {comments_rating}')
        print(f'Рейтинг всех комментариев к статьям автора - {posts_comment_rating}')

        self.rating = posts_rating * 3 + comments_rating + posts_comment_rating
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length = 100, unique = True)


class Post(models.Model):
    news = "NW"
    article = "AR"

    POST_TYPES = [
        (news, "Новость"),
        (article, "Статья")]

    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    choice_field = models.CharField(max_length = 2, choices = POST_TYPES, default = news)
    time_of_text_creation = models.DateTimeField(auto_now_add = True)
    relation_with_post_and_category = models.ManyToManyField(Category, through = "PostCategory")
    article_title = models.CharField(max_length = 255)
    article_text = models.TextField()
    rating = models.IntegerField(default = 0)

    def preview(self):
        preview_text = self.article_text[0:124] + '...'
        return preview_text

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment_text = models.TextField()
    time_of_comment_creation = models.DateTimeField(auto_now_add = True)
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
