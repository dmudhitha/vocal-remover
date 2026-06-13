import subprocess
import sys
import os
import shutil
from pathlib import Path

REQUIRED_PACKAGES = [
    "fastapi",
    "uvicorn",
    "python-multipart",
    "demucs",
    "torch==2.1.2",
    "torchaudio==2.1.2",
    "numpy==1.26.4",
    "ffmpeg-python",
    "soundfile"
]

def check_ffmpeg():
    print("--- Checking FFmpeg ---")
    if shutil.which("ffmpeg"):
        print("✓ FFmpeg is installed.")
        return True
    else:
        print("✗ FFmpeg NOT found in PATH.")
        print("Please install FFmpeg (https://ffmpeg.org/) and add it to your System PATH.")
        return False

def install_packages():
    print("--- Checking/Installing Python Dependencies ---")
    for package in REQUIRED_PACKAGES:
        try:
            # For packages with versions, just check the name
            name = package.split("==")[0]
            __import__(name.replace("-", "_"))
            print(f"✓ {package} is already installed.")
        except ImportError:
            print(f"Installing {package}...")
            try:
                # Use --index-url for torch/torchaudio to ensure CPU versions on Windows if needed
                if "torch" in package:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--index-url", "https://download.pytorch.org/whl/cpu"])
                else:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✓ Successfully installed {package}")
            except Exception as e:
                print(f"✗ Failed to install {package}: {e}")
                return False
    return True

def run_diagnostic():
    print("\n--- Running Diagnostics ---")
    try:
        import torch
        import torchaudio
        import numpy
        import demucs
        print(f"Python version: {sys.version}")
        print(f"PyTorch version: {torch.__version__}")
        print(f"Torchaudio version: {torchaudio.__version__}")
        print(f"NumPy version: {numpy.__version__}")
        print(f"Demucs version: {demucs.__version__}")
        
        # Test if we can import the separation module
        from demucs.separate import main as demucs_main
        print("✓ AI separation module loaded successfully.")
        return True
    except Exception as e:
        print(f"✗ Diagnostic failed: {e}")
        return False

def main():
    print("========================================")
    print("   Voice Remover App - Setup Tool")
    print("========================================\n")

    if not check_ffmpeg():
        sys.exit(1)

    if not install_packages():
        print("\n✗ Setup failed during package installation.")
        sys.exit(1)

    if run_diagnostic():
        print("\n" + "="*40)
        print("✅ SETUP COMPLETE & VERIFIED!")
        print("="*40)
        print("\nYou can now run the tool using either:")
        print("1. Web UI: python backend/main.py")
        print("2. CLI:    python cli/vocal_remover.py [file_path]")
        print("="*40)
    else:
        print("\n✗ Setup completed but diagnostics failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
