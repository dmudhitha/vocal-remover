import { useState, useRef, ChangeEvent, DragEvent } from 'react';
import './App.css';

interface SeparationResult {
  vocals: string;
  instrumental: string;
  filename: string;
}

const API_BASE = "http://localhost:8000";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<SeparationResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setResult(null);
      setError(null);
    }
  };

  const handleDragOver = (e: DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.name.toLowerCase().endsWith('.mp3') || 
          droppedFile.name.toLowerCase().endsWith('.wav')) {
        setFile(droppedFile);
        setResult(null);
        setError(null);
      } else {
        setError("Please upload an MP3 or WAV file.");
      }
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleProcess = async () => {
    if (!file) return;

    setIsLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE}/api/separate`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Separation failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="title">Vocal Remover</h1>
      <p className="subtitle">High-quality audio source separation powered by AI</p>

      {!result && (
        <div 
          className={`upload-card ${isDragging ? 'dragging' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleUploadClick}
        >
          <input 
            type="file" 
            className="file-input" 
            ref={fileInputRef}
            onChange={handleFileChange}
            accept=".mp3,.wav"
          />
          <div className="upload-icon">🎵</div>
          {file ? (
            <p>Selected: <strong>{file.name}</strong></p>
          ) : (
            <p>Drag & drop an MP3 file here, or click to browse</p>
          )}
        </div>
      )}

      {file && !isLoading && !result && (
        <button className="button" onClick={handleProcess}>
          Process Audio
        </button>
      )}

      {isLoading && (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Processing your audio with Demucs AI...</p>
          <p><small>(This may take a few minutes depending on file length)</small></p>
        </div>
      )}

      {error && (
        <div className="error-message">
          Error: {error}
        </div>
      )}

      {result && (
        <div className="results-container">
          <div className="result-item">
            <h3>Vocals</h3>
            <audio controls src={`${API_BASE}${result.vocals}`}></audio>
            <a 
              href={`${API_BASE}${result.vocals}`} 
              download={`${result.filename}_vocals.wav`}
              className="download-link"
            >
              Download Vocals
            </a>
          </div>

          <div className="result-item">
            <h3>Instrumental</h3>
            <audio controls src={`${API_BASE}${result.instrumental}`}></audio>
            <a 
              href={`${API_BASE}${result.instrumental}`} 
              download={`${result.filename}_instrumental.wav`}
              className="download-link"
            >
              Download Instrumental
            </a>
          </div>

          <button className="button" onClick={() => {setResult(null); setFile(null);}}>
            Process Another File
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
