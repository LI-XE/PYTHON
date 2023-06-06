from django.db import models
from datetime import datetime
import re
import bcrypt


class UserManager(models.Manager):
    def register_validator(self, form):
        errors = {}

        if len(form["username"]) < 3:
            errors["username"] = "Username must be at least 3 characters."

        if len(form["alios"]) < 3:
            errors["alios"] = "Alios must be at least 3 characters."

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = "Invalid email address!"

        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use"

        if len(form['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'

        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'

        return errors

    def login_validator(self, form):
        errors = {}
        existing_users = User.objects.filter(email=form["email"])
        if len(form["email"]) == 0:
            errors["email"] = "Email required."
        if len(existing_users) == 0:
            errors["does_not_exist"] = "Please enter a valid email or password."
        if existing_users:
            if len(form["password"]) < 8:
                errors["password"] = "Password must be at least 8 characters."
            elif not bcrypt.checkpw(form["password"].encode(), existing_users[0].password.encode()):
                errors["mismatch"] = "please enter a valid email or password."

        return errors


class User(models.Model):
    username = models.CharField(max_length=255)
    alios = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class BookManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form["title"]) < 2:
            errors["title"] = "Title must be at least 2 characters"

        return errors


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        User, related_name="books", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

    def __str__(self):  # usually only needed if using in admin
        return "{} by {}".format(self.title, self.author)


class ReviewManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form["review"]) < 2:
            errors["review"] = "Review must be at least 2 characters"

        return errors


class Review(models.Model):
    review = models.TextField(max_length=255, null=True)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewer = models.ForeignKey(
        User, related_name="reviews", on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, related_name="book_reviews", on_delete=models.CASCADE)
    objects = ReviewManager()

    def __str__(self):  # usually only needed if using in admin
        return "{} by {}".format(self.review, self.rating, self.reviewer)
