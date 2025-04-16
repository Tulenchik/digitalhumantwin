# This software is licensed under a **dual-license model**
# For individuals and businesses earning **under $1M per year**, this software is licensed under the **MIT License**
# Businesses or organizations with **annual revenue of $1,000,000 or more** must obtain permission to use this software commercially.

# llm_to_face.py
import sys
import os
import traceback

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    # Import pygame
    import pygame
    
    # Import keyboard
    import keyboard
    
    import time
    import string
    
    from livelink.animations.default_animation import stop_default_animation
    
    from utils.stt.transcribe_whisper import transcribe_audio
    
    from utils.audio.record_audio import record_audio_until_release
    
    from utils.vector_db.vector_db import vector_db
    
    from utils.llm.turn_processing import process_turn
    
    from utils.llm.llm_initialiser import initialize_system
    
    from utils.tts.kokoro_server import start_kokoro_server, dummy_kokoro_server
    
    from config import (
        BASE_SYSTEM_MESSAGE, 
        get_llm_config, 
        setup_warnings, 
        USE_OLLAMA, 
        USE_KOKORO
    )
except Exception as e:
    print(f"ERROR during imports: {e}")
    print(traceback.format_exc())
    sys.exit(1)

try:
    setup_warnings()
    
    llm_config = get_llm_config(system_message=BASE_SYSTEM_MESSAGE)
except Exception as e:
    print(f"ERROR during config setup: {e}")
    print(traceback.format_exc())
    sys.exit(1)

def main():
    try:
        # Start Kokoro TTS server if configured
        kokoro_server_thread = None
        if USE_KOKORO:
            print("Starting Kokoro TTS server...")
            try:
                kokoro_server_thread = start_kokoro_server()
                if kokoro_server_thread:
                    print("Kokoro TTS server started successfully")
                else:
                    print("Using fallback TTS (Kokoro server not available)")
            except Exception as e:
                print(f"WARNING: Error starting Kokoro: {e}")
                print("Using fallback TTS instead")
        
        # Initialize the system
        print("Starting system initialization...")
        system_objects = initialize_system()
        print("System initialized successfully")
        
        socket_connection = system_objects['socket_connection']
        full_history = system_objects['full_history']
        chat_history = system_objects['chat_history']
        chunk_queue = system_objects['chunk_queue']
        audio_queue = system_objects['audio_queue']
        tts_worker_thread = system_objects['tts_worker_thread']
        audio_worker_thread = system_objects['audio_worker_thread']
        default_animation_thread = system_objects['default_animation_thread']
        
        # Show LLM and TTS configuration
        if USE_OLLAMA:
            print(f"Using Ollama LLM: {llm_config['OLLAMA_MODEL']}")
        else:
            print(f"Using {'local' if llm_config['USE_LOCAL_LLM'] else 'OpenAI'} LLM")
        
        if USE_KOKORO and kokoro_server_thread:
            print("Using Kokoro TTS")
        else:
            print(f"Using {'local' if system_objects.get('USE_LOCAL_AUDIO', True) else 'ElevenLabs'} TTS")
        
        # Choose input mode
        mode = ""
        try:
            while mode not in ['t', 'r']:
                mode = input("Choose input mode: 't' for text, 'r' for push-to-talk, 'q' to quit: ").strip().lower()
                if mode == 'q':
                    return
        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting.")
            return
        
        print(f"Selected mode: {mode}")
        
        try:
            while True:
                try:
                    if mode == 'r':
                        print("\n\nPush-to-talk mode: press/hold Right Ctrl to record, release to finish.")
                        try:
                            while not keyboard.is_pressed('right ctrl'):
                                if keyboard.is_pressed('q'):
                                    print("Recording cancelled. Exiting push-to-talk mode.")
                                    return
                                time.sleep(0.01)
                            audio_bytes = record_audio_until_release()
                            transcription, _ = transcribe_audio(audio_bytes)
                            if transcription:
                                user_input = transcription
                            else:
                                print("Transcription failed. Make sure you have a stt api and it's correctly set in utils > stt > transcribe_whisper.py. Please try again.")
                                continue
                        except Exception as e:
                            print(f"Error in recording/transcription: {e}")
                            user_input = input("\n\nFallback to text input due to error. Enter text (or 'q' to quit): ").strip()
                            if user_input.lower() == 'q':
                                break
                    else:
                        user_input = input("\n\nEnter text (or 'q' to quit): ").strip()
                        if user_input.lower() == 'q':
                            break

                    chat_history = process_turn(user_input, chat_history, full_history, llm_config, chunk_queue, audio_queue, vector_db, base_system_message=BASE_SYSTEM_MESSAGE)
                except KeyboardInterrupt:
                    print("\nInterrupted by user. Exiting.")
                    break
                except Exception as e:
                    print(f"Error processing turn: {e}")
                    print("Continuing to next turn...")
                    continue

        finally:
            # Clean up resources
            print("Cleaning up resources...")
            try:
                chunk_queue.join()
                chunk_queue.put(None)
                tts_worker_thread.join()
                audio_queue.join()
                audio_queue.put(None)
                audio_worker_thread.join()
                stop_default_animation.set()
                default_animation_thread.join()
                pygame.quit()
                socket_connection.close()
                print("Cleanup complete")
            except Exception as e:
                print(f"Error during cleanup: {e}")
    except Exception as e:
        print(f"ERROR in main function: {e}")
        print(traceback.format_exc())
        
if __name__ == "__main__":
    try:
        print("Starting NeuroSync Player...")
        main()
        print("NeuroSync Player has shut down")
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        print(traceback.format_exc())
