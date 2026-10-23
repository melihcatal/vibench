from observability_client import clients
from typing import List

def embed_log_messages(log_messages: List[str], model_name: str = "embed-english-v3.0") -> List[List[float]]:
    """
    Embeds selected log messages for semantic retrieval using Cohere Embed.
    """
    cohere_client = clients.cohere_client
    
    try:
        response = cohere_client.embed(
            texts=log_messages,
            model=model_name,
            input_type="classification"
        )
        return response.embeddings
    except Exception as e:
        print(f"Error embedding messages: {e}")
        return [[] for _ in log_messages]
