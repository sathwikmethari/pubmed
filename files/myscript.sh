#!/bin/bash
echo "Available commands
run : Runs the main file.
-h or --help : Display usage instructions.
-f or --file : Specify the filename.
"
read -p ">> " input
if [[ "$input" == "run" ]]; then
    echo "Running Python script..."
    python3 example.py
elif [[ "$input" == "-h" || "$input" == "--help" ]]; then
    echo "Will add help later!"

elif [[ "$input" == "-f" || "$input" == "--file" ]]; then
    echo "will add later!"
    date

else
    echo "Unrecognized command."
fi
