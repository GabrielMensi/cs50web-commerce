#!/bin/bash

# Script to reset and repopulate test data for the auction site

echo "🧹 Completely resetting database and populating fresh data..."

# Remove the database file to ensure a complete fresh start
if [ -f "db.sqlite3" ]; then
    echo "Removing existing database..."
    rm db.sqlite3
fi

# Recreate the database with migrations
echo "Running migrations..."
.venv/bin/python manage.py migrate

# Populate with fresh test data
echo "Populating test data..."
.venv/bin/python manage.py populate_testdata

echo ""
echo "✅ Done!"
echo ""
echo "Available test accounts:"
echo "   • alice (password: testpass123)"
echo "   • bob (password: testpass123)"  
echo "   • charlie (password: testpass123)"
echo "   • diana (password: testpass123)"
echo "   • admin (password: testpass123) - superuser"
echo ""
echo "Page: http://localhost:8000"
echo "Admin: http://localhost:8000/admin/"
