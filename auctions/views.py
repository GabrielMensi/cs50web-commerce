from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def index(request):
    listings = Listing.objects.filter(active=True)
    categories = Category.objects.all()
    return render(
        request,
        "auctions/index.html",
        {
            "listings": listings,
            "categories": categories
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="login")
def create_listing(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/createListing.html", {
            "categories": categories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        category = Category.objects.get(name=request.POST["category"])
        owner = request.user

        # Primero creamos el Listing sin el precio inicial
        listing = Listing(
            title=title,
            description=description,
            image=image,
            category=category,
            owner=owner
        )
        listing.save()

        # Luego creamos el Bid y lo asociamos al Listing
        bid_amount = float(request.POST["price"])
        bid = Bid(bid=bid_amount, user=owner, listing=listing)
        bid.save()

        # Asignamos el Bid creado como el precio inicial del Listing
        listing.price = bid
        listing.save()
        return HttpResponseRedirect(reverse("index"))


def listing(request, id):
    listing = get_object_or_404(Listing, id=id)
    isListingInWatchlist = request.user in listing.watchlist.all()
    comments = listing.listing_comments.all()
    isOwner = request.user == listing.owner
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "isListingInWatchlist": isListingInWatchlist,
        "comments": comments,
        "isOwner": isOwner
    })


def displayCategory(request):
    if request.method == "POST":
        category_name = request.POST["category"]
        category = Category.objects.get(name=category_name)
        listings = Listing.objects.filter(active=True, category=category)
        categories = Category.objects.all()
        return render(
            request,
            "auctions/index.html",
            {
                "listings": listings,
                "categories": categories
            })


@login_required(login_url="login")
def removeWatchlist(request, id):
    listing = Listing.objects.get(id=id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))


@login_required(login_url="login")
def addWatchlist(request, id):
    listing = Listing.objects.get(id=id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))


@login_required(login_url="login")
def watchlist(request):
    listings = request.user.watchlist_listings.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def addComment(request, id):
    listing = Listing.objects.get(id=id)
    user = request.user
    comment = request.POST["comment"]
    comment = Comment(
        comment=comment,
        listing=listing,
        user=user
    )
    comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))


def addBid(request, id):
    listing = Listing.objects.get(id=id)
    bid = float(request.POST["bid"])
    comments = listing.listing_comments.all()
    isListingInWatchlist = request.user in listing.watchlist.all()
    isOwner = request.user == listing.owner
    if bid > listing.price.bid:
        listing.price.bid = bid
        listing.price.save()
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "success bid",
            "update": True,
            "comments": comments,
            "isListingInWatchlist": isListingInWatchlist,
            "isOwner": isOwner
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "bid must be greater than current bid",
            "update": False,
            "comments": comments,
            "isListingInWatchlist": isListingInWatchlist,
            "isOwner": isOwner
        })


def closeAuction(request, id):
    listing = Listing.objects.get(id=id)
    listing.active = False
    listing.save()
    comments = listing.listing_comments.all()
    isListingInWatchlist = request.user in listing.watchlist.all()
    isOwner = request.user == listing.owner
    return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Auction closed successfully",
            "update": True,
            "comments": comments,
            "isListingInWatchlist": isListingInWatchlist,
            "isOwner": isOwner
    })
