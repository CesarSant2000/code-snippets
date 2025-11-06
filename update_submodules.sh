#!/bin/bash

# Check if the base branch is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <base-branch>"
    exit 1
fi

BASE_BRANCH=$1
CURRENT_MONTH=$(date +%m)
BRANCH_NAME="2025-${CURRENT_MONTH}-CS-UPDATE-SUBMODULES"

# Ensure the current directory is a Git repository
if [ ! -d "$PWD/.git" ]; then
    echo "Error: The current directory is not a Git repository."
    exit 1
fi

# Remove all local branches
echo "Removing all local branches..."
git branch | grep -v "\*" | xargs -r git branch -D

# Switch to the base branch
echo "Switching to base branch: $BASE_BRANCH..."
git checkout "$BASE_BRANCH"

# Pull the latest changes from origin
echo "Pulling latest changes from origin..."
git pull origin "$BASE_BRANCH"

# Create a new branch
echo "Creating new branch: $BRANCH_NAME..."
git checkout -b "$BRANCH_NAME"

# Update submodules
echo "Updating submodules..."
git submodule update --remote --recursive --force

# Commit changes
echo "Committing changes..."
git commit -am "[IMP][CS] Update submodules"

# Push the new branch to origin
echo "Pushing branch to origin..."
git push --set-upstream origin "$BRANCH_NAME"

echo "Submodule update process completed successfully."
