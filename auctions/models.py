from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_bids"
    )
    listing = models.ForeignKey(
        "Listing",
        on_delete=models.CASCADE,
        related_name="listing_bids"
    )

    def __str__(self):
        return f"{self.user} bid {self.bid} on {self.listing}"

    def delete(self, *args, **kwargs):
        listing = self.listing
        super().delete(*args, **kwargs)
        # Obtener la Bid más alta restante para la Listing
        highest_bid = listing.listing_bids.order_by('-bid').first()
        # Actualizar el precio de la Listing
        listing.price = highest_bid
        listing.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Obtener la Bid más alta actual para la Listing
        highest_bid = self.listing.listing_bids.order_by('-bid').first()
        # Actualizar el precio de la Listing
        self.listing.price = highest_bid
        self.listing.save()


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    price = models.ForeignKey(
        Bid,
        on_delete=models.SET_NULL,
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
    winner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="winner_listings"
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
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
