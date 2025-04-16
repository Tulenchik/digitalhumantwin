import requests
import base64
import os
import sys
import tempfile
import numpy as np
import soundfile as sf
from pathlib import Path

# Make sure the parent directory is in the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from config import TRANSCRIPTION_SERVER_URL, USE_LOCAL_WHISPER, WHISPER_MODEL_SIZE

# Local Whisper model
try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    print("faster-whisper not installed. To use local speech recognition, install it with:")
    print("pip install faster-whisper")
    WHISPER_AVAILABLE = False

# Path to store the whisper model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "whisper_model")
MODEL_SIZE = WHISPER_MODEL_SIZE  # Use the size from config

def ensure_whisper_model():
    """Check if the model exists - faster-whisper will download it automatically if needed"""
    if not WHISPER_AVAILABLE:
        return False
    
    os.makedirs(MODEL_PATH, exist_ok=True)
    return True

def transcribe_audio_locally(audio_bytes, return_timestamps=False):
    """Transcribe audio with optional timestamps using local Whisper."""
    if not WHISPER_AVAILABLE:
        print("faster-whisper not available. Please install it with: pip install faster-whisper")
        return None, None
        
    if not ensure_whisper_model():
        print("Could not initialize whisper model")
        return None, None
        
    try:
        # First, we need to save the audio bytes to a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name
        
        try:
            # Load audio file
            audio_data, sample_rate = sf.read(temp_audio_path)
            
            # Initialize the Whisper model
            # Use compute_type="int8" for CPU, "float16" for GPU
            model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8", download_root=MODEL_PATH)
            
            # Transcribe
            segments, info = model.transcribe(temp_audio_path, beam_size=5, word_timestamps=return_timestamps)
            
            # Process results
            transcription = ""
            timestamps = []
            
            for segment in segments:
                transcription += segment.text + " "
                
                if return_timestamps and segment.words:
                    for word in segment.words:
                        timestamps.append({
                            "start": word.start,
                            "end": word.end,
                            "text": word.word
                        })
            
            transcription = transcription.strip()
            return transcription, timestamps if return_timestamps else None
                
        finally:
            # Clean up the temporary file
            os.unlink(temp_audio_path)
    
    except Exception as e:
        print(f"Local transcription error: {e}")
        return None, None

def transcribe_audio_remotely(audio_bytes, return_timestamps=False):
    """Transcribe audio using the remote server."""
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    try:
        response = requests.post(
            TRANSCRIPTION_SERVER_URL,
            json={
                'audio_base64': audio_base64,
                'return_timestamps': return_timestamps
            }
        )

        if response.status_code == 200:
            response_data = response.json()
            transcription = response_data.get('transcription', '').strip()
            timestamps = response_data.get('timestamps', [])
            return transcription, timestamps if return_timestamps else None

        print(f"Error: Server returned status code {response.status_code}.")
    except requests.exceptions.RequestException as e:
        print(f"Remote transcription failed with exception: {e}")

    return None, None

def transcribe_audio(audio_bytes, return_timestamps=False):
    """
    Transcribe audio with optional timestamps.
    
    Tries local transcription first if enabled, falls back to remote server if local fails
    or is not enabled.
    """
    if USE_LOCAL_WHISPER:
        # Try local transcription first
        transcription, timestamps = transcribe_audio_locally(audio_bytes, return_timestamps)
        if transcription:
            return transcription, timestamps
        
        # If local transcription failed and we have a server URL, try remote
        print("Local transcription failed. Attempting remote transcription...")
    
    # Fall back to remote transcription
    return transcribe_audio_remotely(audio_bytes, return_timestamps)

def transcribe_and_save_audio(audio_path, long_form=False):
    """Save transcription and optionally timestamps."""
    transcription_path = audio_path.replace('.wav', '.txt')

    if os.path.exists(transcription_path):
        return '' 

    with open(audio_path, 'rb') as audio_file:
        audio_bytes = audio_file.read()

    transcription, timestamps = transcribe_audio(audio_bytes, return_timestamps=long_form)
    print(f"Audio transcribed: {transcription[:50]}...")  

    if transcription:
        with open(transcription_path, 'w') as transcription_file:
            transcription_file.write(transcription)

        # Optionally, save timestamps to a separate file
        if long_form and timestamps:
            timestamp_path = audio_path.replace('.wav', '_timestamps.txt')
            with open(timestamp_path, 'w') as timestamp_file:
                for segment in timestamps:
                    timestamp_file.write(f"[{segment['start']}s - {segment['end']}s]: {segment['text']}\n")

    return transcription
