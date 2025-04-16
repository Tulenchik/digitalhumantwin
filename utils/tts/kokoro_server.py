# utils/tts/kokoro_server.py
import sys
import os
import threading

def start_kokoro_server():
    """
    Start the Kokoro TTS server in a separate thread.
    """
    print("DEBUG: Attempting to start Kokoro TTS server...")
    
    try:
        # Dynamically import to handle errors gracefully
        from utils.tts.kokoro.kokoro_api import app_kokoro, run_kokoro_app
        
        # Start server in a separate thread
        server_thread = threading.Thread(target=run_kokoro_app)
        server_thread.daemon = True
        server_thread.start()
        print("DEBUG: Kokoro TTS server started successfully")
        return server_thread
    except ImportError as e:
        print(f"WARNING: Could not import Kokoro TTS modules: {e}")
        print("INFO: Kokoro TTS will not be available. Using fallback TTS if configured.")
        return None
    except Exception as e:
        print(f"WARNING: Error starting Kokoro TTS server: {e}")
        print("INFO: Kokoro TTS will not be available. Using fallback TTS if configured.")
        return None

# Dummy implementation to use when Kokoro is not available
def dummy_kokoro_server():
    """Dummy function that acts as a placeholder for the Kokoro server."""
    print("DEBUG: Using dummy Kokoro TTS server")
    return None

if __name__ == '__main__':
    # Run the server directly when this script is executed
    print("Starting Kokoro TTS server...")
    thread = start_kokoro_server()
    if thread:
        thread.join() 