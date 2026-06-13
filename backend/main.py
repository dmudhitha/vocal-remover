import os
import shutil
import subprocess
import uvicorn
import sys
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# CORS configuration for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
PROCESSED_DIR = BASE_DIR / "processed"

UPLOAD_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)

# Serve processed files via /output
app.mount("/output", StaticFiles(directory=PROCESSED_DIR), name="output")

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.post("/api/separate")
async def separate_audio(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".mp3", ".wav", ".m4a")):
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload MP3, WAV or M4A.")
    
    file_path = UPLOAD_DIR / file.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {str(e)}")
    
    # Run Demucs
    # --two-stems=vocals will output vocals and no_vocals
    # -o processed
    # htdemucs is the default model in v4
    try:
        model_name = "htdemucs"
        command = [
            sys.executable, "-m", "demucs.separate",
            "--two-stems", "vocals",
            "-n", model_name,
            "-o", str(PROCESSED_DIR),
            str(file_path)
        ]
        
        # Set environment variable for UTF-8 encoding to avoid Windows charmap errors
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        # This will block until finished. In a real app, we'd use a task queue.
        # But for this prototype, we'll run it synchronously.
        result = subprocess.run(command, capture_output=True, text=True, env=env)
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "Unknown separation error"
            print(f"Demucs Error: {error_msg}")
            raise HTTPException(status_code=500, detail=f"Separation failed: {error_msg}")

        filename_no_ext = Path(file.filename).stem
        
        # The output path is: PROCESSED_DIR / model_name / filename_no_ext / ...
        output_subdir = PROCESSED_DIR / model_name / filename_no_ext
        
        if not output_subdir.exists():
             # Fallback: find the most recent directory in PROCESSED_DIR / model_name
             model_dir = PROCESSED_DIR / model_name
             if model_dir.exists():
                 subdirs = sorted(model_dir.iterdir(), key=os.path.getmtime, reverse=True)
                 if subdirs:
                     output_subdir = subdirs[0]
                     filename_no_ext = output_subdir.name

        vocals_path = f"/output/{model_name}/{filename_no_ext}/vocals.wav"
        instrumental_path = f"/output/{model_name}/{filename_no_ext}/no_vocals.wav"
        
        return {
            "success": True,
            "vocals": vocals_path,
            "instrumental": instrumental_path,
            "filename": filename_no_ext
        }
        
    except Exception as e:
        print(f"Internal Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
