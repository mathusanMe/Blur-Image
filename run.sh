#!/bin/bash

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Display menu for user to choose which script to run
echo -e "${YELLOW}Select an option:${NC}"
echo -e "1) ${GREEN}Run core${NC}"
echo -e "2) ${GREEN}Run Fast core${NC}"
echo -e "3) ${GREEN}Run Fast blind core${NC}"
echo -e "4) ${GREEN}Run both fast core and fast blind core${NC}"
read -p "Enter option: " option

# Path to Python scripts
ACTIVATE_VENV="source blur_image_env/bin/activate"
CORE_SCRIPT="python3 core.py"
FAST_CORE_SCRIPT="python3 fast_core.py"
FAST_BLIND_CORE_SCRIPT="python3 fast_blind_core.py"

# Execute based on user input
case $option in
    1)
        echo -e "${YELLOW}Running core...${NC}"
        $ACTIVATE_VENV
        $CORE_SCRIPT
        ;;
    2)
        echo -e "${YELLOW}Running fast_core...${NC}"
        $ACTIVATE_VENV
        $FAST_CORE_SCRIPT
        ;;
    3)
        echo -e "${YELLOW}Running fast_blind_core...${NC}"
        $ACTIVATE_VENV
        $FAST_BLIND_CORE_SCRIPT
        ;;
    4)
        echo -e "${YELLOW}Running both fast_core and fast_blind_core...${NC}"
        $ACTIVATE_VENV
        $FAST_CORE_SCRIPT
        $FAST_BLIND_CORE_SCRIPT
        $BLIND_CORE_SCRIPT
        ;;
    *)
        echo -e "${RED}Invalid option selected. Exiting.${NC}"
        exit 1
        ;;
esac
