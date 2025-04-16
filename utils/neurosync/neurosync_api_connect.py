# This software is licensed under a **dual-license model**
# For individuals and businesses earning **under $1M per year**, this software is licensed under the **MIT License**
# Businesses or organizations with **annual revenue of $1,000,000 or more** must obtain permission to use this software commercially.

import requests
import json
import os

# Define constants directly instead of importing them from config
NEUROSYNC_LOCAL_URL = "http://127.0.0.1:5000/audio_to_blendshapes"
NEUROSYNC_REMOTE_URL = "https://api.neurosync.info/audio_to_blendshapes" 
NEUROSYNC_API_KEY = os.getenv("NEUROSYNC_API_KEY", "YOUR-NEUROSYNC-API-KEY")

def send_audio_to_neurosync(audio_bytes, use_local=True):
    """
    Send audio bytes to the NeuroSync API for processing into blendshapes.
    
    Uses the local API by default, but can use the remote API if specified.
    
    Args:
        audio_bytes (bytes): The audio data to process
        use_local (bool): Whether to use the local API endpoint (default: True)
        
    Returns:
        list or None: Parsed facial data if successful, None otherwise
    """
    try:
        # Use the local or remote URL depending on the flag
        url = NEUROSYNC_LOCAL_URL if use_local else NEUROSYNC_REMOTE_URL
        headers = {}
        if not use_local:
            headers["API-Key"] = NEUROSYNC_API_KEY

        if not validate_audio_bytes(audio_bytes):
            print("Error: Invalid audio data")
            return None
            
        response = post_audio_bytes(audio_bytes, url, headers)
        response.raise_for_status()  
        json_response = response.json()
        return parse_blendshapes_from_json(json_response)

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return None
    except Exception as e:
        print(f"Error in send_audio_to_neurosync: {e}")
        return None

def validate_audio_bytes(audio_bytes):
    """Check if audio_bytes is valid."""
    return audio_bytes is not None and len(audio_bytes) > 0

def post_audio_bytes(audio_bytes, url, headers):
    """Post audio bytes to the given URL with headers."""
    headers["Content-Type"] = "application/octet-stream"
    response = requests.post(url, headers=headers, data=audio_bytes)
    return response

def parse_blendshapes_from_json(json_response):
    """Parse the blendshapes from the JSON response."""
    blendshapes = json_response.get("blendshapes", [])
    facial_data = []

    for frame in blendshapes:
        frame_data = [float(value) for value in frame]
        facial_data.append(frame_data)

    return facial_data
