#!/bin/bash
# Quick start script for macOS/Linux

echo "========================================"
echo "Financial Insights Agent - Quick Start"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Check if requirements are installed
echo "Checking dependencies..."
if ! pip show streamlit > /dev/null 2>&1; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and add your API keys."
    echo ""
    exit 1
fi

# Run the application
echo "Starting Financial Insights Agent..."
echo ""
echo "The app will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py
