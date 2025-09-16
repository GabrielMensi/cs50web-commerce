# Commerce

This project is an e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a watchlist.

## Table of Contents

- [Commerce](#commerce)
  - [Table of Contents](#table-of-contents)
  - [Video Presentation](#video-presentation)
  - [Features](#features)
  - [Installation](#installation)
  - [Quick Start with Test Data](#quick-start-with-test-data)
  - [Usage](#usage)
  - [Test Accounts](#test-accounts)
  - [Development](#development)
  - [Specification](#specification)

## Video Presentation

You can see the video [Here](https://youtu.be/1iQOUcSqI1I)

## Features

- User authentication (register, login, logout)
- Create auction listings with images and categories
- Place bids on active auctions
- Add/remove items from personal watchlist
- Comment on auction listings
- Close auctions (listing owners only)
- Browse by categories
- Admin interface for site management

## Installation

To install and set up the project, follow these steps:

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository to your local machine:**

```bash
git clone https://github.com/GabrielMensi/cs50web-commerce.git
```

2. **Navigate to the project directory:**

```bash
cd cs50web-commerce
```

3. **Create a virtual environment (recommended):**

```bash
python -m venv .venv
```

4. **Activate the virtual environment:**

On Linux/macOS:
```bash
source .venv/bin/activate
```

On Windows:
```bash
.venv\Scripts\activate
```

5. **Install the required dependencies:**

```bash
pip install -r requirements.txt
```

6. **Apply database migrations:**

```bash
python manage.py migrate
```

7. **Create a superuser account (optional, for admin access):**

```bash
python manage.py createsuperuser
```

## Quick Start with Test Data

For a quick demonstration of the auction site with sample data, use the provided test data script:

### Automatic Setup with Test Data

```bash
# Make the script executable (Linux/macOS only)
chmod +x reset_testdata.sh

# Run the script
./reset_testdata.sh
```

This script will:
- Remove any existing database
- Create a fresh database with migrations
- Populate the site with sample auction listings, categories, bids, and comments
- Create test user accounts

### Manual Test Data Setup

If you prefer to set up test data manually:

```bash
# Reset the database
rm db.sqlite3  # Remove existing database (if any)
python manage.py migrate

# Populate with test data
python manage.py populate_testdata
```

## Usage

1. **Start the development server:**

```bash
python manage.py runserver
```

2. **Open your web browser and navigate to:**
   - Main site: http://localhost:8000
   - Admin interface: http://localhost:8000/admin/

## Test Accounts

After running the test data setup, you can use these pre-created accounts:

| Username | Password | Role |
|----------|----------|------|
| alice | testpass123 | Regular user |
| bob | testpass123 | Regular user |
| charlie | testpass123 | Regular user |
| diana | testpass123 | Regular user |
| admin | testpass123 | Superuser (admin access) |

## Development

### Project Structure

```
commerce/
├── auctions/           # Main application
│   ├── models.py      # Database models
│   ├── views.py       # View functions
│   ├── urls.py        # URL routing
│   ├── forms.py       # Django forms
│   └── templates/     # HTML templates
├── commerce/          # Django project settings
├── requirements.txt   # Python dependencies
└── manage.py         # Django management script
```

### Key Commands

```bash
# Run development server
python manage.py runserver

# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Access Django shell
python manage.py shell

# Reset and repopulate test data
./reset_testdata.sh
```

## Specification

You must fulfill the following requirements:

- [x]   **Models**: Your application should have at least three models in addition to the `User` model: one for auction listings, one for bids, and one for comments made on auction listings. It’s up to you to decide what fields each model should have, and what the types of those fields should be. You may have additional models if you would like.
- [x]   **Create Listing**: Users should be able to visit a page to create a new listing. They should be able to specify a title for the listing, a text-based description, and what the starting bid should be. Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
- [x]   **Active Listings Page**: The default route of your web application should let users view all of the currently active auction listings. For each active listing, this page should display (at minimum) the title, description, current price, and photo (if one exists for the listing).
- [x]   **Listing Page**: Clicking on a listing should take users to a page specific to that listing. On that page, users should be able to view all details about the listing, including the current price for the listing.
    - [x]   If the user is signed in, the user should be able to add the item to their “Watchlist.” If the item is already on the watchlist, the user should be able to remove it.
    - [x]   If the user is signed in, the user should be able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user should be presented with an error.
    - [x]  If the user is signed in and is the one who created the listing, the user should have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
    - [x]  If a user is signed in on a closed listing page, and the user has won that auction, the page should say so.
    - [x]  Users who are signed in should be able to add comments to the listing page. The listing page should display all comments that have been made on the listing.
- [x]  **Watchlist**: Users who are signed in should be able to visit a Watchlist page, which should display all of the listings that a user has added to their watchlist. Clicking on any of those listings should take the user to that listing’s page.
- [x]  **Categories**: Users should be able to visit a page that displays a list of all listing categories. Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.
- [x]  **Django Admin Interface**: Via the Django admin interface, a site administrator should be able to view, add, edit, and delete any listings, comments, and bids made on the site.
-> Listing: create, edit, delete
-> comments: create, delete, edit
-> bids: create, edit, delete
