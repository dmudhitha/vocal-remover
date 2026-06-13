import argparse
import os
import subprocess
import sys
from pathlib import Path

def separate_audio(input_file, output_dir, model_name="htdemucs"):
    """
    Separates vocals from an audio file using Demucs.
    """
    input_path = Path(input_file).resolve()
    if not input_path.exists():
        print(f"Error: Input file '{input_file}' not found.")
        return False

    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"--- Processing: {input_path.name} ---")
    print(f"Using model: {model_name}")
    print("This may take a few minutes...")

    # Set environment variable for UTF-8 encoding to avoid Windows charmap errors
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    # Construct Demucs command
    # Using sys.executable to ensure we use the same environment
    command = [
        sys.executable, "-m", "demucs.separate",
        "--two-stems", "vocals",
        "-n", model_name,
        "-o", str(output_path),
        str(input_path)
    ]

    try:
        # Run the process and stream output to the console
        process = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            env=env,
            encoding='utf-8',
            errors='replace'
        )

        # Print output in real-time
        for line in process.stdout:
            print(line, end="")

        process.wait()
        
        if process.returncode != 0:
            print(f"\nSeparation Failed with exit code {process.returncode}")
            return False

        # Success!
        filename_no_ext = input_path.stem
        final_dir = output_path / model_name / filename_no_ext
        
        print("\n" + "="*50)
        print("SUCCESS! Files created in:")
        print(f"  {final_dir}")
        print("\nTracks:")
        print(f"  - Vocals: {final_dir / 'vocals.wav'}")
        print(f"  - Instrumental: {final_dir / 'no_vocals.wav'}")
        print("="*50)
        return True

    except Exception as e:
        print(f"\nAn internal error occurred: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Voice Remover CLI - Separate vocals from any MP3/WAV file.")
    parser.add_argument("input", help="Path to the input audio file (MP3, WAV, etc.)")
    parser.add_argument("-o", "--output", default="output", help="Directory to save the separated tracks (default: 'output')")
    parser.add_argument("-m", "--model", default="htdemucs", help="Demucs model to use (default: htdemucs)")

    # If no arguments are provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    success = separate_audio(args.input, args.output, args.model)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
