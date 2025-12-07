#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate

find . -type f -name "requirements.txt" | while read -r req_file; do
    echo "Installing dependencies from $req_file"
    pip install -r "$req_file"
done

echo "Python virtual environment created and dependencies installed."
echo "To activate it, run: source .venv/bin/activate"
