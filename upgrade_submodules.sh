#!/bin/bash

# ==============================================================================
# Script Name: upgrade_submodules
# Description: COMPLETE LIFECYCLE MANAGEMENT (ROBUST VERSION)
#              1. Safely handles local changes.
#              2. HANDLES BROKEN SUBMODULES during checkout (Fixes "fatal: not a git repo").
#              3. Cleans old submodules (Deep Clean).
#              4. Adds new submodule (Smart Path).
#              5. Auto-PR.
# ==============================================================================

# --- Configuration: Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# --- Variables for PR Description ---
DELETED_LOG=""
ADDED_LOG=""

# --- Helper Functions ---
log_info() { echo -e "${BLUE}[INFO] $1${NC}"; }
log_success() { echo -e "${GREEN}[OK] $1${NC}"; }
log_warn() { echo -e "${YELLOW}[WARN] $1${NC}"; }
log_error() { echo -e "${RED}[ERROR] $1${NC}"; exit 1; }
log_step() { echo -e "\n${CYAN}=== $1 ===${NC}"; }

# --- 1. Parameter Validation ---
if [ $# -lt 2 ]; then
    echo -e "${RED}Usage Error: Missing parameters.${NC}"
    echo -e "Syntax: ./upgrade_submodules ${YELLOW}<BASE_BRANCH> <REMOVE_LIST_CSV> [NEW_URL] [NEW_BRANCH]${NC}"
    exit 1
fi

BASE_BRANCH="$1"
REMOVE_LIST="$2"
NEW_SUB_URL="$3"
NEW_SUB_BRANCH="$4"

# --- 2. Environment Setup ---
log_step "Step 1: Environment & Safety Check"

GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$GIT_ROOT" ]; then
    log_error "Not a git repository."
fi
cd "$GIT_ROOT" || log_error "Could not change directory to git root."

CURRENT_BRANCH=$(git branch --show-current)
log_info "Current Branch: $CURRENT_BRANCH"

# Check if workspace is dirty
if [[ -n $(git status --porcelain) ]]; then
    log_warn "Uncommitted changes detected."
    
    if [[ "$CURRENT_BRANCH" == "$BASE_BRANCH" ]]; then
        log_warn "Stashing changes on base branch..."
        git stash push -m "Auto-stash by upgrade_submodules $(date +%F_%T)"
    else
        log_warn "Saving WIP on feature branch..."
        git add .
        git commit -m "WIP: Saving work before submodule upgrade"
        git push -u origin "$CURRENT_BRANCH"
    fi
fi

# --- 3. Sync with Base Branch (ROBUST) ---
log_step "Step 2: Syncing Base Branch ($BASE_BRANCH)"

if [[ "$CURRENT_BRANCH" != "$BASE_BRANCH" ]]; then
    log_info "Attempting to switch to $BASE_BRANCH..."
    
    # Intento 1: Checkout Normal
    if ! git checkout "$BASE_BRANCH" 2>/dev/null; then
        log_warn "Standard checkout failed (likely due to broken submodule folders)."
        log_info "Attempting surgical cleanup of broken paths..."
        
        # Intento 2: Limpieza Quirúrgica
        # Si Git se queja de las carpetas que vamos a borrar de todas formas, las borramos YA.
        IFS=',' read -ra AD_HOC_SUBS <<< "$REMOVE_LIST"
        for path in "${AD_HOC_SUBS[@]}"; do
            path=$(echo "$path" | xargs)
            path=${path%/}
            if [ -d "$path" ]; then
                echo "   -> Removing obstacle: $path"
                rm -rf "$path"
            fi
        done

        # Limpieza de directorios no rastreados que bloquean
        git clean -ffd

        log_info "Retrying checkout with force..."
        git checkout -f "$BASE_BRANCH" || log_error "Failed to checkout even after cleanup. Repo state is critical."
    fi
fi

log_info "Pulling latest changes..."
git pull origin "$BASE_BRANCH" || log_error "Failed to pull changes."

# --- 4. Create Feature Branch ---
CURRENT_DATE=$(date +%Y-%m-%d)
NEW_BRANCH_NAME="${CURRENT_DATE}-CS-UPGRADE-SUBMODULES"

log_step "Step 3: Creating Branch ($NEW_BRANCH_NAME)"

if git show-ref --verify --quiet "refs/heads/$NEW_BRANCH_NAME"; then
    log_warn "Branch exists. Recreating it..."
    git branch -D "$NEW_BRANCH_NAME"
fi

git checkout -b "$NEW_BRANCH_NAME"

# --- 5. Remove Submodules ---
log_step "Step 4: Removing Submodules"

IFS=',' read -ra SUBS <<< "$REMOVE_LIST"

for path in "${SUBS[@]}"; do
    path=$(echo "$path" | xargs)
    path=${path%/} 

    if [ -z "$path" ]; then continue; fi
    echo -e "Processing: ${YELLOW}$path${NC}"

    # Force cleanup even if git doesn't recognize it
    if [ -d "$path" ]; then
        # Check if it has a broken .git file
        if [ -f "$path/.git" ]; then
             # Remove the broken .git file reference so git deinit works or doesn't complain
             rm -f "$path/.git"
        fi
    fi

    # Cleaning logic
    git submodule deinit -f -- "$path" 2>/dev/null
    git rm -f "$path" 2>/dev/null
    
    # Fallback cleanup
    if [ $? -ne 0 ]; then
         git config -f .gitmodules --remove-section "submodule.$path" 2>/dev/null
         git rm --cached "$path" 2>/dev/null
         rm -rf "$path"
    fi

    rm -rf ".git/modules/$path"
    
    DELETED_LOG+="- $path\n"
    log_success "Submodule '$path' removed."
done

# --- 6. Add New Submodule ---
log_step "Step 5: Adding New Submodule"

if [ -n "$NEW_SUB_URL" ]; then
    if [ -z "$NEW_SUB_BRANCH" ]; then
        log_error "Missing Branch parameter."
    fi

    TEMP_PATH=$(echo "$NEW_SUB_URL" | sed -E 's#^.*[:/]([^/]+/[^/]+)(\.git)?$#\1#')
    TARGET_PATH=${TEMP_PATH%.git}

    if [ -z "$TARGET_PATH" ]; then
        log_error "Could not determine target path."
    fi

    log_info "Installing to: ${YELLOW}$TARGET_PATH${NC}"
    
    git submodule add --force -b "$NEW_SUB_BRANCH" "$NEW_SUB_URL" "$TARGET_PATH"
    
    if [ $? -eq 0 ]; then
        ADDED_LOG="- $TARGET_PATH (Branch: $NEW_SUB_BRANCH)\n"
        log_success "Submodule added successfully."
    else
        log_error "Failed to add submodule."
    fi
else
    log_info "No new submodule to add."
    ADDED_LOG="No new submodules added."
fi

# --- 7. Auto Commit & Push ---
log_step "Step 6: Committing and Pushing"

git add .
COMMIT_MSG="[REF] Upgrade submodules ${CURRENT_DATE}"

log_info "Committing..."
git commit -m "$COMMIT_MSG"

log_info "Pushing..."
git push -u origin "$NEW_BRANCH_NAME"

# --- 8. Create Pull Request ---
log_step "Step 7: Creating Pull Request"

PR_TITLE="[REF] Upgrade Submodules ${CURRENT_DATE}"
PR_BODY="### Submodule Upgrade Report

**Removed Submodules:**
${DELETED_LOG}

**Added Submodules:**
${ADDED_LOG}

_Auto-generated by upgrade_submodules script_"

if command -v gh &> /dev/null; then
    gh pr create --base "$BASE_BRANCH" --head "$NEW_BRANCH_NAME" --title "$PR_TITLE" --body "$PR_BODY"
    if [ $? -eq 0 ]; then log_success "PR Created!"; else log_warn "CLI PR failed."; fi
else
    log_warn "GitHub CLI not found."
fi

REPO_URL=$(git config --get remote.origin.url)
if [[ "$REPO_URL" == git@* ]]; then
    REPO_URL=${REPO_URL/:/\/}
    REPO_URL=${REPO_URL/git@/https:\/\/}
    REPO_URL=${REPO_URL%.git}
fi

PR_URL="${REPO_URL}/compare/${BASE_BRANCH}...${NEW_BRANCH_NAME}?expand=1"

echo -e "\n${BLUE}==============================================${NC}"
echo -e "${GREEN}Process Complete!${NC}"
echo -e "Manual PR Link:\n${YELLOW}${PR_URL}${NC}"
echo -e "${BLUE}==============================================${NC}"