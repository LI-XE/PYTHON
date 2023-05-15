from django.db import models


class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    shoe_size = models.IntegerField()
    is_half_size = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Shoe(models.Model):
    brand = models.CharField(max_length=45)
    color = models.CharField(max_length=17)
    material = models.CharField(max_length=17)
    has_laces = models.BooleanField()
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # created_by = models.ForeignKey(User, related_name="shoes_created", on_delete=models.CASCADE)
    # owner = models.ForeignKey(User, related_name="shoes_owned", on_delete=models.CASCADE)
