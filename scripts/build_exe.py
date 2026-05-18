import PyInstaller.__main__
import os
import sys

def build():
    print("[*] Starting Pulse Windows Build (.exe)...")
    
    # Path to the main entry point
    entry_point = os.path.join('src', 'pulse', 'cli.py')
    
    # PyInstaller arguments
    params = [
        entry_point,
        '--onefile',
        '--name=pulse',
        '--console',
        '--clean',
        '--add-data=src/pulse:pulse' # Include the package data
    ]
    
    PyInstaller.__main__.run(params)
    print("[+] Build complete. Check the 'dist' folder for pulse.exe")

if __name__ == "__main__":
    if sys.platform != 'win32' and '--force' not in sys.argv:
        print("[!] Warning: This script is intended to run on Windows.")
        print("[*] If you want to build on Linux for Windows, use Wine or cross-compilation tools.")
        print("[*] Running with --force to attempt local build.")
        if '--force' not in sys.argv:
            sys.exit(1)
    
    build()
