from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_bids"
    )


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    price = models.ForeignKey(
        Bid,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="price_listings"
    )
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
    watchlist = models.ManyToManyField(
        User,
        blank=True,
        related_name="watchlist_listings"
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
        return f"{self.user} commented on {self.listing}"
