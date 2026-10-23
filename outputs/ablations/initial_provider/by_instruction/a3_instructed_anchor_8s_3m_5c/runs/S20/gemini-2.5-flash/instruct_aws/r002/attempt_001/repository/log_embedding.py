from observability_client import get_openai_client
from typing import List, Dict
import os

def embed_log_messages(log_messages: List[str], model: str = "text-embedding-ada-002") -> Dict[str, List[float]]:
    client = get_openai_client()
    
    embeddings = {}
    for i, message in enumerate(log_messages):
        if not message.strip():
            embeddings[f"log_message_{i}"] = []
            continue
        
        try:
            response = client.embeddings.create(
                input=message,
                model=model
            )
            embeddings[f"log_message_{i}"] = response.data[0].embedding
        except Exception as e:
            print(f"Error embedding log message {i}: {e}")
            embeddings[f"log_message_{i}"] = [] # Return empty list on error
    return embeddings
