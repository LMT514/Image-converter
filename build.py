# build.py
import PyInstaller.__main__
import os
import shutil
import platform

# Configure paths
script_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(script_dir, "build")
dist_dir = os.path.join(script_dir, "dist")
icon_path = os.path.join(script_dir, "convert-icon.ico")

# Clean previous builds
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)
if os.path.exists(dist_dir):
    shutil.rmtree(dist_dir)

# PyInstaller configuration
args = [
    "main_app.py",           # Entry point
    "--onefile",             # Single executable
    "--windowed",            # No console window
    f"--icon={icon_path}",   # Application icon
    "--name=FileConverter",  # Output name
    "--add-data=convert-icon.ico;.",  # Include icon
]

# Add OS-specific arguments
if platform.system() == "Windows":
    args += ["--add-binary=ffmpeg.exe;."]  # Include FFmpeg for Windows

# Run PyInstaller
PyInstaller.__main__.run(args)

print("\nBuild complete! Executable is in the 'dist' folder.")