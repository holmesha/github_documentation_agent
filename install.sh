#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create .env file
if [ ! -f .env ]; then
    echo "OPENAI_API_KEY=your-api-key-here" > .env
    echo "Created .env file. Please update with your OpenAI API key."
else
    echo ".env file already exists."
fi

# Set execute permissions for app.py
chmod +x readme_generator.py

echo "Installation complete. Run the app with: python3 readme_generator.py"
