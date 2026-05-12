#!/bin/bash

# Change to project root
cd "$(dirname "$0")/.."

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

# Auto-download fonts if missing
if ! ls src/material-dark/fonts/*.ttf &>/dev/null; then
    echo "Downloading fonts..."
    python3 scripts/download_fonts.py
fi

python3 scripts/make-resource.py \
    -base-dir src/material-dark \
    -style style.qss \
    -config config.json \
    -variables variables.json \
    -icons-dir icons \
    -output Material-Dark.qbtheme \
    -dir-prefix "/uitheme"
