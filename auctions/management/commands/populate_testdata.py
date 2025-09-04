from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from auctions.models import Category, Listing, Bid, Comment

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with test data for the auction site'

    def handle(self, *args, **options):
        # Create superuser first
        self.stdout.write('Creating superuser...')
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('testpass123')
            admin_user.save()
            self.stdout.write(f'Created superuser: {admin_user.username}')
        else:
            self.stdout.write(f'Superuser already exists: {admin_user.username}')

        # Create categories
        categories_data = [
            'Electronics',
            'Fashion',
            'Home & Garden',
            'Sports',
            'Books',
            'Toys',
            'Automotive',
            'Art & Collectibles'
        ]

        categories = {}
        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(name=cat_name)
            categories[cat_name] = category
            if created:
                self.stdout.write(f'Created category: {cat_name}')

        # Create test users
        users_data = [
            {
                'username': 'alice',
                'email': 'alice@example.com',
                'password': 'testpass123'
            },
            {
                'username': 'bob',
                'email': 'bob@example.com',
                'password': 'testpass123'
            },
            {
                'username': 'charlie',
                'email': 'charlie@example.com',
                'password': 'testpass123'
            },
            {
                'username': 'diana',
                'email': 'diana@example.com',
                'password': 'testpass123'
            }
        ]

        users = {}
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email']
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            users[user_data['username']] = user

        # Create test listings
        listings_data = [
            {
                'title': 'Vintage iPhone 12',
                'description': 'Excellent iPhone 12 with box. No scratches.',
                'starting_price': Decimal('350.00'),
                'image': 'https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500',  # noqa
                'category': 'Electronics',
                'owner': 'alice',
                'active': True
            },
            {
                'title': 'Designer Leather Jacket',
                'description': 'Genuine leather jacket. Size M, worn twice.',
                'starting_price': Decimal('120.00'),
                'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500',  # noqa
                'category': 'Fashion',
                'owner': 'bob',
                'active': True
            },
            {
                'title': 'Mountain Bike - Trek',
                'description': 'Quality bike for trails and city.',
                'starting_price': Decimal('450.00'),
                'image': 'https://images.unsplash.com/photo-1534150034764-046bf225d3fa?w=500',  # noqa
                'category': 'Sports',
                'owner': 'charlie',
                'active': True
            },
            {
                'title': 'Antique Chess Set',
                'description': 'Wooden chess set from 1960s. Minor wear.',
                'starting_price': Decimal('75.00'),
                'image': 'https://images.unsplash.com/photo-1413919873593-061d76ec8452?w=500',  # noqa
                'category': 'Art & Collectibles',
                'owner': 'diana',
                'active': True
            },
            {
                'title': 'Gaming Laptop - ASUS ROG',
                'description': 'Gaming laptop with RTX 3070, 16GB RAM.',
                'starting_price': Decimal('800.00'),
                'image': 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500',  # noqa
                'category': 'Electronics',
                'owner': 'alice',
                'active': True
            },
            {
                'title': 'Vintage Record Collection',
                'description': '50+ vinyl records from 70s-80s.',
                'starting_price': Decimal('200.00'),
                'image': 'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=500',  # noqa
                'category': 'Art & Collectibles',
                'owner': 'bob',
                'active': False  # This will be a closed auction
            },
            {
                'title': 'Professional Camera Kit',
                'description': 'Canon EOS R5 with lens and tripod.',
                'starting_price': Decimal('1500.00'),
                'image': 'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=500',  # noqa
                'category': 'Electronics',
                'owner': 'charlie',
                'active': True
            },
            {
                'title': 'Handmade Ceramic Vase',
                'description': 'Unique ceramic vase by local artist.',
                'starting_price': Decimal('45.00'),
                'image': 'https://images.unsplash.com/photo-1608110546381-a29025c9e878?q=80&w=500',  # noqa
                'category': 'Home & Garden',
                'owner': 'diana',
                'active': True
            }
        ]

        listings = {}
        for listing_data in listings_data:
            listing, created = Listing.objects.get_or_create(
                title=listing_data['title'],
                owner=users[listing_data['owner']],
                defaults={
                    'description': listing_data['description'],
                    'starting_price': listing_data['starting_price'],
                    'image': listing_data['image'],
                    'category': categories[listing_data['category']],
                    'active': listing_data['active']
                }
            )

            if created:
                self.stdout.write(f'Created listing: {listing.title}')
            else:
                self.stdout.write(f'Listing already exists: {listing.title}')
            
            listings[listing_data['title']] = listing

        # Add some additional bids to make it more realistic
        additional_bids = [
            {
                'listing_title': 'Vintage iPhone 12',
                'bidder': 'bob',
                'amount': Decimal('375.00')
            },
            {
                'listing_title': 'Vintage iPhone 12',
                'bidder': 'charlie',
                'amount': Decimal('400.00')
            },
            {
                'listing_title': 'Designer Leather Jacket',
                'bidder': 'alice',
                'amount': Decimal('135.00')
            },
            {
                'listing_title': 'Mountain Bike - Trek',
                'bidder': 'diana',
                'amount': Decimal('475.00')
            },
            {
                'listing_title': 'Mountain Bike - Trek',
                'bidder': 'alice',
                'amount': Decimal('500.00')
            },
            {
                'listing_title': 'Gaming Laptop - ASUS ROG',
                'bidder': 'bob',
                'amount': Decimal('850.00')
            },
            {
                'listing_title': 'Gaming Laptop - ASUS ROG',
                'bidder': 'diana',
                'amount': Decimal('900.00')
            },
            # Closed auction bids
            {
                'listing_title': 'Vintage Record Collection',
                'bidder': 'alice',
                'amount': Decimal('225.00')
            },
            {
                'listing_title': 'Vintage Record Collection',
                'bidder': 'charlie',
                'amount': Decimal('250.00')
            }
        ]

        for bid_data in additional_bids:
            listing = listings[bid_data['listing_title']]
            bidder = users[bid_data['bidder']]
            Bid.objects.create(
                bid=bid_data['amount'],
                user=bidder,
                listing=listing
            )
            # The bid.save() method will automatically update listing.price
            self.stdout.write(
                f'Added bid: ${bid_data["amount"]} by {bidder.username}'
            )

        # Close the vintage record collection auction and set winner
        closed_listing = listings['Vintage Record Collection']
        closed_listing.active = False
        highest_bid = closed_listing.listing_bids.order_by('-bid').first()
        closed_listing.winner = highest_bid.user
        closed_listing.save()
        self.stdout.write(
            f'Closed auction: {closed_listing.title}, '
            f'winner: {closed_listing.winner.username}'
        )

        # Add some comments with realistic timestamps
        now = timezone.now()
        comments_data = [
            {
                'listing_title': 'Vintage iPhone 12',
                'user': 'bob',
                'comment': 'Does this come with the original charger?',
                'created_at': now - timedelta(hours=3)
            },
            {
                'listing_title': 'Vintage iPhone 12',
                'user': 'alice',
                'comment': 'Yes, it includes the original cable and adapter!',
                'created_at': now - timedelta(hours=2, minutes=30)
            },
            {
                'listing_title': 'Designer Leather Jacket',
                'user': 'charlie',
                'comment': 'What brand is this jacket?',
                'created_at': now - timedelta(days=1, hours=5)
            },
            {
                'listing_title': 'Mountain Bike - Trek',
                'user': 'alice',
                'comment': 'Beautiful bike! What year is it?',
                'created_at': now - timedelta(days=2, hours=8)
            },
            {
                'listing_title': 'Gaming Laptop - ASUS ROG',
                'user': 'diana',
                'comment': 'Can this run the latest games at high settings?',
                'created_at': now - timedelta(minutes=45)
            }
        ]

        for comment_data in comments_data:
            listing = listings[comment_data['listing_title']]
            user = users[comment_data['user']]
            comment = Comment.objects.create(
                comment=comment_data['comment'],
                listing=listing,
                user=user
            )
            # Set the created_at timestamp manually after creation
            comment.created_at = comment_data['created_at']
            comment.save()
            self.stdout.write(f'Added comment by {user.username}')

        # Add some items to watchlists
        watchlist_data = [
            {'user': 'alice', 'listing_title': 'Mountain Bike - Trek'},
            {'user': 'alice', 'listing_title': 'Professional Camera Kit'},
            {'user': 'bob', 'listing_title': 'Gaming Laptop - ASUS ROG'},
            {'user': 'bob', 'listing_title': 'Antique Chess Set'},
            {'user': 'charlie', 'listing_title': 'Designer Leather Jacket'},
            {'user': 'charlie', 'listing_title': 'Vintage iPhone 12'},
            {'user': 'diana', 'listing_title': 'Vintage iPhone 12'},
        ]

        for watch_data in watchlist_data:
            user = users[watch_data['user']]
            listing = listings[watch_data['listing_title']]
            listing.watchlist.add(user)
            self.stdout.write(f'Added to {user.username}\'s watchlist')

        self.stdout.write(
            self.style.SUCCESS(
                '\nTest data populated successfully!\n'
                'You can now:\n'
                '1. Visit http://localhost:8000 to see active listings\n'
                '2. Login with test users (alice, bob, charlie, diana) '
                'using password: testpass123\n'
                '3. Login as admin (username: admin, password: admin123) '
                'for superuser access\n'
                '4. Test bidding, watchlist, and commenting features\n'
                '5. Access admin panel at http://localhost:8000/admin/ '
                'with the admin account'
            )
        )
