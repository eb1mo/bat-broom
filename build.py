#!/usr/bin/env python3
"""
Build script for creating Bat Broom executable
"""

import os
import sys
import subprocess
import shutil

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Install PyInstaller"""
    print("Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building Bat Broom executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=BatBroom",
        "--icon=broom.ico",  # Optional: if icon file exists
        "bat_broom.py"
    ]
    
    # Remove icon parameter if file doesn't exist
    if not os.path.exists("broom.ico"):
        cmd.remove("--icon=broom.ico")
    
    try:
        subprocess.check_call(cmd)
        print("✅ Build completed successfully!")
        print("📁 Executable location: dist/BatBroom.exe")
        
        # Clean up build files
        if os.path.exists("build"):
            shutil.rmtree("build")
            print("🧹 Cleaned up build directory")
        
        if os.path.exists("BatBroom.spec"):
            os.remove("BatBroom.spec")
            print("🧹 Cleaned up spec file")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

def main():
    """Main build function"""
    print("🧹 Bat Broom Build Script")
    print("=" * 30)
    
    # Check if PyInstaller is installed
    if not check_pyinstaller():
        print("PyInstaller not found. Installing...")
        try:
            install_pyinstaller()
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyInstaller")
            return 1
    
    # Check if main file exists
    if not os.path.exists("bat_broom.py"):
        print("❌ bat_broom.py not found in current directory")
        return 1
    
    # Build executable
    if build_executable():
        print("\n🎉 Build completed successfully!")
        print("You can now run: dist/BatBroom.exe")
        return 0
    else:
        print("\n❌ Build failed")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 