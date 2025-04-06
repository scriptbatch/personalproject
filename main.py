import os
import sys
import subprocess
import ctypes
import tkinter as tk
from tkinter import messagebox

def is_admin():
    """Check if the current user has admin privileges."""
    if os.name == 'nt':
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    return False

def request_admin():
    """Use Tkinter to request admin privileges if the user doesn't have them."""
    if not is_admin():
        # Create Tkinter window (it won't be shown, but needed for dialogs)
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        # Ask for admin privileges
        response = messagebox.askquestion(
            "Admin Privileges",
            "This program requires administrator rights to function properly.\n\nDo you want to grant admin privileges?"
        )

        if response == 'yes':
            # Run the script as administrator using the UAC prompt (only once)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, sys.argv[0], None, 1)
            sys.exit(0)  # Exit the current process so that the new elevated process runs
        else:
            messagebox.showerror(
                "Admin Rights Required",
                "You need to grant admin rights for this script to work properly.\nExiting the program."
            )
            sys.exit(1)  # Exit the program as we can't proceed without admin privileges

def run_scripts():
    """Run the scripts."""
    subprocess.run(["python3", "script1.py"])
    subprocess.run(["python3", "script2.py"])

if __name__ == "__main__":
    # Request admin rights before running the main functionality
    request_admin()

    # Run the scripts after admin privileges are granted
    run_scripts()
