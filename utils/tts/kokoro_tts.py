# utils/tts/kokoro_tts.py
import requests
import json

def get_kokoro_audio(text, voice_id="af_bella"):
    """
    Calls the Kokoro TTS API to generate speech for the given text.
    
    Args:
        text (str): The text to convert to speech
        voice_id (str): The voice ID to use (default: "af_bella")
        
    Returns:
        bytes or None: The audio data if successful, None otherwise
    """
    # Kokoro TTS endpoint from the kokoro_api.py implementation
    KOKORO_TTS_URL = "http://localhost:8000/generate_speech"
    
    payload = {
        "text": text
        # The Kokoro API as implemented doesn't support voice selection via the API
        # It's configured in the kokoro_api.py implementation directly
    }
    
    try:
        response = requests.post(KOKORO_TTS_URL, json=payload)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Error calling Kokoro TTS: {e}")
        return None 