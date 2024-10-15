#!/bin/bash

while true; do
    # Check for changes
    git add .
    git commit -m "Auto-commit on $(date +"%Y-%m-%d %H:%M:%S")" --allow-empty
    git push origin main # Change 'main' to your branch name if different
    
    # Sleep for a specified interval (e.g., 60 seconds)
    sleep 60
done
