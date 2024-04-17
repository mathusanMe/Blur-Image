#!/bin/bash

# Display menu for user to choose which script to run
echo "Select an option:"
echo "1) Run core"
echo "2) Run blind_core"
echo "3) Run both"
read -p "Enter option: " option

# Path to Python scripts
CORE_SCRIPT="python3 blur_image/core.py"
BLIND_CORE_SCRIPT="python3 blur_image/blind_core.py"

# Execute based on user input
case $option in
    1)
        echo "Running core..."
        $CORE_SCRIPT
        ;;
    2)
        echo "Running blind_core..."
        $BLIND_CORE_SCRIPT
        ;;
    3)
        echo "Running both core and blind_core..."
        $CORE_SCRIPT
        $BLIND_CORE_SCRIPT
        ;;
    *)
        echo "Invalid option selected. Exiting."
        exit 1
        ;;
esac
