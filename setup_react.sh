#!/bin/bash

echo "🚀 Setting up React Frontend for CM Assistant"

# Navigate to React directory
cd frontend-react

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo "✅ npm version: $(npm --version)"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
    echo ""
    echo "🎉 Setup complete! To start the application:"
    echo ""
    echo "   cd frontend-react"
    echo "   npm start"
    echo ""
    echo "Then open http://localhost:3000 in your browser"
    echo ""
    echo "⚠️ Make sure the backend is running on http://localhost:8000"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi