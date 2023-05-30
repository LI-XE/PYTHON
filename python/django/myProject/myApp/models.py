from django.db import models
from datetime import datetime
import re
import bcrypt


class UserManager(models.Manager):
    def register_validator(self, form):
        errors = {}

        if len(form["username"]) < 3:
            errors["username"] = "Username must be at least 3 characters."

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
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Shoe(models.Model):
    brand = models.CharField(max_length=45)
    color = models.CharField(max_length=17)
    material = models.CharField(max_length=17)
    has_laces = models.BooleanField()
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ShowManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form["title"]) < 2:
            errors["title"] = "Title must be at least 2 characters"

        if len(form["network"]) < 3:
            errors["network"] = "Network should be at least 3 characters"

        if len(form["description"]) > 0 and len(form["description"]) < 10:
            errors["description"] = "Description must be at least 10 characters"

        if form["release_date"] == "":
            errors["release_date"] = "Release Date should not be blank!"
        else:
            release_date = datetime.strptime(form["release_date"], "%Y-%m-%d")
            if release_date > datetime.now():
                errors["release_date"] = "Invalid Date(Release Date must be a past date)"

        return errors


class Show(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    release_date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, related_name="shows_created", on_delete=models.CASCADE)
    guests = models.ManyToManyField(User, related_name="shows")
    objects = ShowManager()

    def __str__(self):  # usually only needed if using in admin
        return "{} by {}".format(self.title, self.network)
