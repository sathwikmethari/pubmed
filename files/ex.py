import subprocess
import os

script_filename = "myscript.sh"

# Step 1: Make the script executable
os.chmod(script_filename, 0o755)

# Step 2: Run the script in a new terminal window
try:
    subprocess.Popen(["gnome-terminal", "--", f"./{script_filename}"])
except FileNotFoundError:
    print("Could not find 'gnome-terminal'. Try 'x-terminal-emulator', 'konsole', or another terminal.")
