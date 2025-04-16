# config.py
import os

# LLM Configuration
USE_LOCAL_LLM = True
USE_STREAMING = True
USE_OLLAMA = True  # New setting to enable Ollama
OLLAMA_MODEL = "llama3.1:8b"  # Model name for Ollama
OLLAMA_API_BASE = "http://localhost:11434"  # Standard Ollama API endpoint

# Original Local LLM endpoints (kept for backward compatibility)
LLM_API_URL = "http://127.0.0.1:5050/generate_llama"
LLM_STREAM_URL = "http://127.0.0.1:5050/generate_stream"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR-KEY-GOES-HERE")

# LLM performance settings
# Reduced chunk length and flush token count for shorter pauses
MAX_CHUNK_LENGTH = 200  # Reduced from 500
FLUSH_TOKEN_COUNT = 80  # Reduced from 300

# TTS Configuration
DEFAULT_VOICE_NAME = 'af_bella'  # Default Kokoro voice
USE_LOCAL_AUDIO = True
USE_KOKORO = True  # New setting to enable Kokoro TTS
LOCAL_TTS_URL = "http://127.0.0.1:8000/generate_speech"  # Updated to match Kokoro endpoint
USE_COMBINED_ENDPOINT = False

# STT Configuration (new)
USE_LOCAL_WHISPER = True  # Set to True to use local Whisper model, False to use server
WHISPER_MODEL_SIZE = "base"  # Options: "tiny", "base", "small", "medium", "large"
TRANSCRIPTION_SERVER_URL = "http://127.0.0.1:6969/transcribe"  # Fallback server URL

ENABLE_EMOTE_CALLS = False
USE_VECTOR_DB = False

# Ollama-specific performance options
OLLAMA_OPTIONS = {
    "num_ctx": 512,       # Smaller context window for faster processing
    "num_predict": 128,   # Limit prediction length
    "top_p": 0.7,         # Lower top_p for more focused responses
    "temperature": 0.5,   # Match the temperature above
    "num_thread": 8,      # Use multiple threads for processing
    "num_batch": 8,       # Use batch processing
    "repeat_penalty": 1.1, # Slight penalty for repetition
    "stop": ["\n", "user:", "assistant:"],  # Stop on common delimiters
    "mirostat": 2,        # Use Mirostat 2.0 for better sampling
    "mirostat_tau": 5.0,  # Target entropy for Mirostat
    "mirostat_eta": 0.1   # Learning rate for Mirostat
}

BASE_SYSTEM_MESSAGE = """
You are Mai, a helpful digital assistant with a personality. Be concise but friendly in your responses, with some light humor. 
Respond briefly but accurately to user questions, and try to be helpful.
When the user asks you to do something you can't do (like sending emails or controlling smart home devices), politely clarify your limitations and offer alternatives if possible.
Since you're a voice-based assistant, keep things conversational. Don't mention formatting, line breaks, or other visual elements.
""".strip()

# ---------------------------
# Emote Sender Configuration (new)
# ---------------------------
EMOTE_SERVER_ADDRESS = "127.0.0.1"
EMOTE_SERVER_PORT = 9000

# ---------------------------
# Embedding Configurations (new)
# ---------------------------
# Toggle between local embeddings and OpenAI embeddings.
USE_OPENAI_EMBEDDING = False
# Local embedding server URL:
EMBEDDING_LOCAL_SERVER_URL = "http://127.0.0.1:7070/get_embedding"
# OpenAI embedding model and size.
EMBEDDING_OPENAI_MODEL = "text-embedding-3-small"
LOCAL_EMBEDDING_SIZE = 768
OPENAI_EMBEDDING_SIZE = 1536

# ---------------------------
# Neurosync API Configurations (new)
# ---------------------------

NEUROSYNC_LOCAL_URL = "http://127.0.0.1:5000/audio_to_blendshapes" # if using the realtime api below, you can still access this endpoint from it, just change the port to 6969

# ---------------------------
# TTS with Blendshapes Endpoint (new)
# ---------------------------
TTS_WITH_BLENDSHAPES_REALTIME_API = "http://127.0.0.1:8000/synthesize_and_blendshapes"

### ignore these
#NEUROSYNC_API_KEY = "YOUR-NEUROSYNC-API-KEY" # ignore this
#NEUROSYNC_REMOTE_URL = "https://api.neurosync.info/audio_to_blendshapes" #ignore this


def get_llm_config(system_message=None):
    """
    Returns a dictionary of LLM configuration parameters.
    
    If no system_message is provided, it defaults to BASE_SYSTEM_MESSAGE.
    """
    if system_message is None:
        system_message = BASE_SYSTEM_MESSAGE
    return {
        "USE_VECTOR_DB": USE_VECTOR_DB,
        "USE_LOCAL_LLM": USE_LOCAL_LLM,
        "USE_STREAMING": USE_STREAMING,
        "USE_OLLAMA": USE_OLLAMA,  # Added Ollama flag
        "OLLAMA_MODEL": OLLAMA_MODEL,  # Added Ollama model
        "OLLAMA_API_BASE": OLLAMA_API_BASE,  # Added Ollama API base
        "options": OLLAMA_OPTIONS,  # Added Ollama options
        "LLM_API_URL": LLM_API_URL,
        "LLM_STREAM_URL": LLM_STREAM_URL,
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "max_chunk_length": MAX_CHUNK_LENGTH,
        "flush_token_count": FLUSH_TOKEN_COUNT,
        "system_message": system_message,
    }


def setup_warnings():
    """
    Set up common warning filters.
    """
    import warnings
    warnings.filterwarnings(
        "ignore", 
        message="Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work"
    )
    
    # Ignore common warnings that clutter the console
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", message=".*numpy.ufunc size changed.*")
    warnings.filterwarnings("ignore", message=".*ssl.SSLCertVerificationError.*")
    warnings.filterwarnings("ignore", message=".*Box bound precision lowered.*")
    warnings.filterwarnings("ignore", message=".*Audio data was clipped during epoch*")
    warnings.filterwarnings("ignore", message=".*Could not match submodel*")
    warnings.filterwarnings("ignore", message=".*tcmalloc: large alloc.*")
    warnings.filterwarnings("ignore", message=".*RuntimeWarning: overflow encountered.*")
