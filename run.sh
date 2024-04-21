#!/bin/bash

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Display menu for user to choose which script to run
echo -e "${YELLOW}Select an option:${NC}"
echo -e "1) ${GREEN}Run core${NC}"
echo -e "2) ${GREEN}Run blind_core${NC}"
echo -e "3) ${GREEN}Run both${NC}"
read -p "Enter option: " option

# Path to Python scripts
CORE_SCRIPT="python3 blur_image/core.py"
BLIND_CORE_SCRIPT="python3 blur_image/blind_core.py"

# Execute based on user input
case $option in
    1)
        echo -e "${YELLOW}Running core...${NC}"
        $CORE_SCRIPT
        ;;
    2)
        echo -e "${YELLOW}Running blind_core...${NC}"
        $BLIND_CORE_SCRIPT
        ;;
    3)
        echo -e "${YELLOW}Running both core and blind_core...${NC}"
        $CORE_SCRIPT
        $BLIND_CORE_SCRIPT
        ;;
    *)
        echo -e "${RED}Invalid option selected. Exiting.${NC}"
        exit 1
        ;;
esac
