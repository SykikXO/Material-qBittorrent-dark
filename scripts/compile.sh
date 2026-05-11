#!/bin/bash

# Change to project root
cd "$(dirname "$0")/.."

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

chmod +x scripts/make-resource.py

python3 scripts/make-resource.py \
    -base-dir src/material-dark \
    -style style.qss \
    -config config.json \
    -variables variables.json \
    -icons-dir icons \
    -output Material-Dark.qbtheme \
    -dir-prefix "/uitheme"
