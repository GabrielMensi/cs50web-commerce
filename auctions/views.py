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
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
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
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
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

        listing = Listing(
            title=title,
            description=description,
            image=image,
            category=category,
            owner=owner
        )
        listing.save()

        bid_amount = float(request.POST["price"])
        bid = Bid(bid=bid_amount, user=owner, listing=listing)
        bid.save()

        listing.price = bid
        listing.save()
        return HttpResponseRedirect(reverse("index"))


def listing(request, id):
    listing = get_object_or_404(Listing, id=id)
    isListingInWatchlist = request.user in listing.watchlist.all()
    comments = listing.listing_comments.all()
    isOwner = request.user == listing.owner
    categories = Category.objects.all()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "isListingInWatchlist": isListingInWatchlist,
        "comments": comments,
        "isOwner": isOwner,
        "categories": categories
    })


def display_category(request):
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
def remove_watchlist(request, id):
    listing = get_object_or_404(Listing, id=id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))


@login_required(login_url="login")
def add_watchlist(request, id):
    listing = get_object_or_404(Listing, id=id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))


@login_required(login_url="login")
def watchlist(request):
    listings = request.user.watchlist_listings.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


@login_required(login_url="login")
def add_comment(request, id):
    listing = get_object_or_404(Listing, id=id)
    user = request.user
    comment_text = request.POST["comment"]
    if comment_text.strip():
        comment = Comment(
            comment=comment_text,
            listing=listing,
            user=user
        )
        comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))


@login_required(login_url="login")
def add_bid(request, id):
    listing = get_object_or_404(Listing, id=id)
    bid_amount = float(request.POST["bid"])
    if bid_amount > listing.price.bid:
        new_bid = Bid(bid=bid_amount, user=request.user, listing=listing)
        new_bid.save()
        listing.price = new_bid
        listing.save()
        message = "Success bid"
        update = True
    else:
        message = "Bid must be greater than current bid"
        update = False
    comments = listing.listing_comments.all()
    isListingInWatchlist = request.user in listing.watchlist.all()
    isOwner = request.user == listing.owner
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "message": message,
        "update": update,
        "comments": comments,
        "isListingInWatchlist": isListingInWatchlist,
        "isOwner": isOwner
    })


@login_required(login_url="login")
def close_auction(request, id):
    listing = get_object_or_404(Listing, id=id)
    if request.user == listing.owner:
        listing.active = False
        listing.save()
        message = "Auction closed successfully"
        update = True
    else:
        message = "Only the owner can close the auction"
        update = False
    comments = listing.listing_comments.all()
    isListingInWatchlist = request.user in listing.watchlist.all()
    isOwner = request.user == listing.owner
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "message": message,
        "update": update,
        "comments": comments,
        "isListingInWatchlist": isListingInWatchlist,
        "isOwner": isOwner
    })
