# 🎵 AI Voice Remover

A high-quality, local audio source separation tool that splits any MP3 or WAV file into **Vocals** and **Instrumental** tracks. Powered by Meta's **Demucs** AI engine.

![Project Preview](https://via.placeholder.com/800x400?text=AI+Voice+Remover+Web+Interface)

## ✨ Features
*   **Web Interface:** Modern React + Vite frontend with drag-and-drop file upload.
*   **CLI Tool:** Fast command-line processing for power users.
*   **High Quality:** Uses the `htdemucs` model for state-of-the-art separation.
*   **Local Processing:** No data leaves your machine; everything is processed locally.
*   **Easy Setup:** Includes a diagnostic and automated setup script for Windows.

## 🛠️ Tech Stack
*   **Backend:** Python 3, FastAPI, Uvicorn
*   **Frontend:** React, TypeScript, Vanilla CSS
*   **AI Engine:** Meta Demucs (HTDemucs v4)
*   **Audio Core:** PyTorch, Torchaudio, FFmpeg

## 📋 Prerequisites
1.  **Python 3.8+**
2.  **Node.js & npm** (for frontend)
3.  **FFmpeg:** Must be installed and added to your System PATH.
    *   *Windows:* Install via [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (use the "full-shared" version).

## 🚀 Quick Start (Windows)

1.  **Run the automated setup:**
    Double-click `setup_and_run.py` or run:
    ```bash
    python setup_and_run.py
    ```
    This will install the correct, stable versions of all dependencies (PyTorch, NumPy, etc.).

2.  **Launch the App:**
    Double-click **`run_vocal_remover.bat`**. This provides a menu to start the Web UI or CLI tool instantly.

## 💻 Usage

### Web Interface
1. Start the servers via the `.bat` file or:
   ```bash
   # Terminal 1
   cd backend && python main.py
   # Terminal 2
   cd frontend && npm run dev
   ```
2. Open `http://localhost:5173` in your browser.
3. Upload your MP3/WAV, wait for processing, and download your tracks.

### Command Line (CLI)
Use the dedicated CLI tool for batch processing or quick usage:
```bash
python cli/vocal_remover.py "path/to/song.mp3" -o "output_folder"
```

## 📂 Project Structure
*   `backend/`: FastAPI server and AI logic.
*   `frontend/`: React + TypeScript web application.
*   `cli/`: Standalone command-line tool.
*   `uploads/`: Temporary storage for uploaded files.
*   `processed/`: Output directory for separated stems.
*   `setup_and_run.py`: Automated dependency manager.
*   `run_vocal_remover.bat`: One-click Windows launcher.

## ⚖️ License
MIT License - feel free to use and modify for your own projects!
