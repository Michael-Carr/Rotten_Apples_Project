from django.db import models
import re

# Create your models here.


class UserManager(models.Manager):
    def validate(self, formData):

        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not EMAIL_REGEX.match(formData['email']):
            errors['invalid_email'] = ("Invalid email address!")
        email_check = self.filter(email=formData['email'])
        if email_check:
            errors['email_in_use'] = "Email already in use"
        if len(formData['username']) < 2:
            errors['username'] = 'Username should be at least 2 characters'
        if len(formData['email']) < 2:
            errors['email'] = 'Email should be at least 2 characters'
        if len(formData['password']) < 2:
            errors['password'] = 'Password should be at least 2 characters'
        if formData['confirm_password'] != formData['password']:
            errors['confirm_password'] = 'confirm password matches'

        return errors


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=125)
    password = models.CharField(max_length=50)
    objects = UserManager()
    # user_posts
    # liked_posts

class VgameManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['title']) < 2:
            errors['title'] = 'Title should be at least 2 characters'
        if len(postData['platform']) < 2:
            errors['platform'] = 'Platforms should be at least 2 characters'
        if len(postData['description']) < 10:
            errors['description'] = 'Description should be at least 10 characters'
        return errors

class Vgame(models.Model):
    title = models.CharField(max_length=75)
    platform = models.CharField(max_length=50)
    release_date = models.DateTimeField()
    description = models.TextField()
    image_url = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = VgameManager()
    # game_reviews

class GameReview(models.Model):
    post = models.TextField()
    poster = models.ForeignKey(User, related_name='user_posts', on_delete=models.CASCADE)
    review = models.ForeignKey(Vgame, related_name='game_reviews', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name='liked_posts')
