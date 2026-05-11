#!/bin/bash

# Material qBittorrent Theme Installer
# Supports multiple color schemes

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paths
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCHEME_DIR="$PROJECT_ROOT/colors"
VARS_FILE="$PROJECT_ROOT/src/material-dark/variables.json"
BUILD_SCRIPT="$PROJECT_ROOT/scripts/compile.sh"
OUTPUT_THEME="Material-Dark.qbtheme"
DEST_DIR="$HOME/.config/qBittorrent/themes"

# Ensure directories exist
mkdir -p "$DEST_DIR"

print_header() {
    echo -e "${CYAN}=======================================${NC}"
    echo -e "${CYAN}   Material qBittorrent Installer      ${NC}"
    echo -e "${CYAN}=======================================${NC}"
}

list_schemes() {
    echo -e "${YELLOW}Available color schemes:${NC}"
    local count=1
    for f in "$SCHEME_DIR"/*.json; do
        name=$(basename "$f" .json)
        echo -e "  $count) ${GREEN}$name${NC}"
        schemes[$count]=$name
        ((count++))
    done
    num_schemes=$((count-1))
}

build_theme() {
    local scheme=$1
    echo -e "\n${BLUE}Building theme with scheme: ${YELLOW}$scheme${NC}"
    
    # Copy variables
    cp "$SCHEME_DIR/$scheme.json" "$VARS_FILE"
    
    # Run build script
    if bash "$BUILD_SCRIPT"; then
        echo -e "${GREEN}Build successful!${NC}"
    else
        echo -e "${RED}Build failed!${NC}"
        exit 1
    fi
}

update_qbt_config() {
    local theme_path=$1
    local config_file="$HOME/.config/qBittorrent/qBittorrent.conf"
    
    if [ -f "$config_file" ]; then
        echo -e "${BLUE}Updating qBittorrent config...${NC}"
        
        # Ensure UseCustomUITheme is true
        if grep -q "General\\\\UseCustomUITheme=" "$config_file"; then
            sed -i 's/General\\UseCustomUITheme=.*/General\\UseCustomUITheme=true/' "$config_file"
        else
            sed -i '/\[Preferences\]/a General\\UseCustomUITheme=true' "$config_file"
        fi
        
        # Update CustomUIThemePath
        if grep -q "General\\\\CustomUIThemePath=" "$config_file"; then
            sed -i "s|General\\\\CustomUIThemePath=.*|General\\\\CustomUIThemePath=$theme_path|" "$config_file"
        else
            sed -i "/\[Preferences\]/a General\\\\CustomUIThemePath=$theme_path" "$config_file"
        fi
        
        echo -e "${GREEN}Config updated!${NC}"
    else
        echo -e "${YELLOW}qBittorrent config not found at $config_file. Skipping config update.${NC}"
    fi
}

install_theme() {
    local scheme=$1
    local target_name="Material-Dark-${scheme^}.qbtheme"
    local full_path="$DEST_DIR/$target_name"
    
    echo -e "${BLUE}Installing to: ${YELLOW}$full_path${NC}"
    cp "$PROJECT_ROOT/$OUTPUT_THEME" "$full_path"
    
    # Check if qbt is running
    if pgrep -x "qbittorrent" > /dev/null; then
        echo -e "${YELLOW}Warning: qBittorrent is currently running.${NC}"
        echo -e "${YELLOW}Changes to the config file might be overwritten when qBittorrent closes.${NC}"
        echo -e "${YELLOW}Please close qBittorrent for the changes to take effect reliably.${NC}"
    fi

    update_qbt_config "$full_path"
    
    echo -e "\n${GREEN}Done!${NC}"
    echo -e "Theme: ${CYAN}$target_name${NC} has been applied."
    echo -e "Restart qBittorrent to see the changes."
}

# Main logic
print_header

declare -a schemes
list_schemes

# Check for argument
selected_scheme=""
if [ -n "$1" ]; then
    if [ -f "$SCHEME_DIR/$1.json" ]; then
        selected_scheme=$1
    else
        echo -e "${RED}Error: Scheme '$1' not found.${NC}"
        exit 1
    fi
else
    echo -ne "\n${YELLOW}Select a scheme (1-$num_schemes): ${NC}"
    read choice
    if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "$num_schemes" ]; then
        selected_scheme=${schemes[$choice]}
    else
        echo -e "${RED}Invalid selection.${NC}"
        exit 1
    fi
fi

build_theme "$selected_scheme"
install_theme "$selected_scheme"
