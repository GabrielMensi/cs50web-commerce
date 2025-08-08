#!/bin/bash

# Script to reset and repopulate test data for the auction site

echo "🧹 Clearing existing test data and populating fresh data..."
python manage.py populate_testdata --clear

echo ""
echo "✅ Done! Your auction site now has fresh test data."
echo ""
echo "🚀 Available test accounts:"
echo "   • alice (password: testpass123)"
echo "   • bob (password: testpass123)"  
echo "   • charlie (password: testpass123)"
echo "   • diana (password: testpass123)"
echo "   • admin (password: admin123) - superuser"
echo ""
echo "🌐 Visit: http://localhost:8000"
echo "⚙️  Admin: http://localhost:8000/admin/"
