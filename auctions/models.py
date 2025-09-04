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
        # Only validate for new bids (not updates), and only for active listings
        if self.pk is None and self.listing.active:  # New bid on active listing
            if self.bid <= self.listing.current_price:
                raise ValueError(f"Bid must be higher than current price of {self.listing.current_price}")
        
        super().save(*args, **kwargs)
        # Update the listing's price to point to the highest bid
        highest_bid = self.listing.listing_bids.order_by('-bid').first()
        self.listing.price = highest_bid
        self.listing.save()


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
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

    @property
    def current_price(self):
        """Returns the current price - either highest bid amount or starting price"""
        if self.price:  # If there are bids
            return self.price.bid
        return self.starting_price
    
    @property
    def highest_bid(self):
        """Returns the highest bid object or None"""
        return self.listing_bids.order_by('-bid').first()

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
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} commented on {self.listing}"
