from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="category_listings"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_listings"
    )

    def __str__(self):
        return self.title


class Comments(models.Model):
    comment = models.CharField(max_length=256)
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="listing_comments"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_comments"
    )

    def __str__(self):
        return self.comment
