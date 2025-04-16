# AI-Driven Facial Animation System

A modular system that combines AI language models with text-to-speech to create interactive face animations, enabling real-time streaming of facial blendshapes into Unreal Engine 5 using LiveLink.

## System Architecture

The system consists of several interconnected components:

### Core Components

1. **Input Processing**
   - Text input via console
   - Voice input via microphone recording (PyAudio)
   - Speech-to-text conversion using Whisper (faster-whisper)

2. **Language Model (LLM)**
   - Local inference via Ollama API
   - Streaming token generation
   - Optional OpenAI API integration
   - Sentence/chunk builder for natural speech segmentation

3. **Text-to-Speech (TTS)**
   - Kokoro TTS for high-quality voice synthesis
   - Speech chunking for natural pauses
   - Configurable voice and speech characteristics

4. **Facial Animation Generation**
   - Audio-to-blendshape conversion
   - Emotion detection and blending
   - Interpolation for smooth transitions
   - 61-point blend shape array generation

5. **Unreal Engine Integration**
   - LiveLink protocol for real-time data streaming
   - Socket-based communication
   - Default animation when idle

### Data Flow

```
Input → LLM → Text Chunks → TTS → Audio Bytes → Blendshape Generation → LiveLink → Unreal Engine
  ↑                                                                          ↓
  └────────────────── Default Animation when Idle ───────────────────────────┘
```

### Threading Architecture

The system operates with multiple concurrent threads:
- Main thread: UI and user interaction
- TTS worker thread: Processes text chunks into audio
- Audio/face worker thread: Processes audio/blendshapes and sends to Unreal
- Default animation thread: Provides idle animation when not speaking

## Technical Requirements

### Hardware Requirements

- **CPU**: Multi-core processor (Intel Core i5/i7/i9 or AMD Ryzen 5/7/9)
- **RAM**: 8GB minimum, 16GB recommended
- **GPU**: 
  - For LLM: NVIDIA GPU with 4GB+ VRAM (if using local LLM)
  - For face rendering: Any modern GPU supporting DirectX 11/12
- **Microphone**: Required for voice input mode
- **Disk Space**: At least 2GB for model files and application

### Software Requirements

- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: Python 3.9+ (Python 3.11 recommended)
- **Package Dependencies**:
  - Core: pygame, keyboard, requests, numpy, PyAudio, flask
  - TTS: kokoro (≥0.8.2), soundfile
  - STT: faster-whisper (≥0.9.0)
  - AI: openai (≥1.0.0) if using OpenAI API
- **External Dependencies**:
  - FFmpeg: Required for audio processing
  - Ollama: Required for local LLM support

### Network Requirements

- **Local Operation**: No internet required when using local models
- **API Mode**: Internet connection if using OpenAI or other cloud APIs
- **Bandwidth**: ~100KB/s when using remote APIs

## Quick Setup

1. **Run the setup check** to verify your environment:
   ```bash
   python setup_check.py
   ```
   This will create any missing files and check for required dependencies.

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install external dependencies**:

   - **FFmpeg**: [Download and install FFmpeg](https://ffmpeg.org/download.html)
   - **Ollama**: [Download and install Ollama](https://ollama.com/)
     ```bash
     # After installing Ollama, pull the desired model:
     ollama pull llama3.1:8b
     ```

4. **Verify installation**:
   ```bash
   python setup_check.py
   ```
   All dependencies should be marked as installed.

## Configuration

The system's behavior can be customized in the `config.py` file:

### LLM Options
```python
# LLM Configuration
USE_LOCAL_LLM = True     # Use a local LLM instead of OpenAI
USE_STREAMING = True     # Enable token streaming for more responsive output
USE_OLLAMA = True        # Use Ollama for local LLMs
OLLAMA_MODEL = "llama3.1:8b"  # Ollama model to use
```

### TTS Options
```python
# TTS Configuration
DEFAULT_VOICE_NAME = 'af_bella'  # Default Kokoro voice
USE_LOCAL_AUDIO = True   # Use local TTS instead of cloud services
USE_KOKORO = True        # Use Kokoro TTS for high-quality speech
```

### Speech Chunk Settings (Adjust for Shorter/Longer Pauses)
```python
# Chunking settings - lower values mean shorter pauses
MAX_CHUNK_LENGTH = 200   # Maximum character length per chunk
FLUSH_TOKEN_COUNT = 80   # Number of tokens before flushing to TTS
```

## Usage

Run the main application to start the system:

```bash
python llm_to_face.py
```

The application will:
1. Start the Kokoro TTS server (if enabled)
2. Initialize the LiveLink connection to Unreal Engine
3. Prompt you to choose an input mode:
   - `t` for text input
   - `r` for push-to-talk (requires microphone)
   - `q` to quit

### Input Modes

- **Text Mode**: Simply type your message and press Enter
- **Push-to-Talk Mode**: Press and hold Right Ctrl while speaking, release when done

## Troubleshooting

### Common Issues

- **Import Errors**: If you see "No module named 'utils.stt'" or similar errors:
  ```bash
  python setup_check.py
  ```
  This will create all necessary `__init__.py` files.

- **TTS Issues**: If you have problems with Kokoro TTS:
  ```bash
  pip install -q kokoro>=0.8.2 soundfile
  ```
  Make sure your system has the appropriate audio libraries.

- **Speech Recognition Issues**: If transcription fails:
  ```bash
  pip install faster-whisper
  ```
  The first run will download the model automatically.

- **Ollama Connection Issues**: Make sure Ollama is running:
  ```bash
  # Check if Ollama is running
  curl http://localhost:11434/api/version
  
  # If not running, start it and pull a model
  ollama serve
  ollama pull llama3.1:8b
  ```

### Still Having Issues?

Check the console output for error messages. The application will provide detailed error information that can help diagnose problems.

## Additional Tools

The system comes with several additional scripts:

- `play_generated_files.py`: Play back previously generated animations
- `text_to_face.py`: Convert text directly to facial animation
- `wave_to_face.py`: Convert WAV audio files to facial animation
- `push_to_talk_to_face.py`: Record speech and convert to facial animation

## Unreal Engine Integration

For proper LiveLink integration with Unreal Engine, you will need:

1. **Unreal Engine**: Version 5.0 or higher
2. **LiveLink Plugin**: Enabled in your Unreal project
3. **LiveLink Face Preset**: Configured to receive facial animation data
4. **LiveLink Source**: Set to TCP with the port matching your configuration
