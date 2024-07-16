#!/bin/bash

# Ensure the public directory is cleared
rm -rf public
mkdir public

# Run your Python script to generate the site
python3 src/main.py

# Change to the public directory and start the server
cd public
python3 -m http.server 8888