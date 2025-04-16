# This software is licensed under a **dual-license model**
# For individuals and businesses earning **under $1M per year**, this software is licensed under the **MIT License**
# Businesses or organizations with **annual revenue of $1,000,000 or more** must obtain permission to use this software commercially.

# utils/vector_db/vector_db_utils.py

from datetime import datetime, timezone

# Create dummy functions for embedding to avoid errors
def get_embedding(text, use_openai=False):
    """
    Dummy function that returns a placeholder embedding vector.
    In a real implementation, this would call an embedding service.
    """
    print("DEBUG: Dummy get_embedding called")
    return [0.0] * 768  # Return a vector of zeros with dimension 768

def update_system_message_with_context(user_input: str, base_system_message: str, vector_db, top_n: int = 4) -> str:
    """
    Returns the base system message with the current time.
    In a real implementation, this would add relevant context from the vector database.
    """
    print("DEBUG: update_system_message_with_context called (simplified version)")
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S GMT")
    return f"{base_system_message}\nThe current time and date is: {current_time}"

def add_exchange_to_vector_db(user_input: str, response: str, vector_db):
    """
    Dummy function that doesn't actually add to the vector DB.
    In a real implementation, this would embed the conversation and store it.
    """
    print("DEBUG: add_exchange_to_vector_db called (no action taken)")
    pass

