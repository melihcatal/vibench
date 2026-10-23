import os
import requests
from typing import List, Dict

def embed_log_messages(messages: List[Dict], model_id: str = "text-embedding-ada-002") -> List[Dict]:
    """Embed selected log messages for semantic retrieval.
    Uses OpenAI Embeddings API as a concrete managed model.
    """
    endpoint = "https://api.openai.com/v1/embeddings"
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY environment variable with your OpenAI key")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    embeddings = []
    # OpenAI expects a list of texts; we pull the message field
    texts = [msg.get("message", "") for msg in messages]
    payload = {
        "model": model_id,
        "input": texts
    }
    resp = requests.post(endpoint, headers=headers, json=payload)
    resp.raise_for_status()
    data = resp.json()
    # Attach the embedding vector back to each log entry
    for log, embedding in zip(messages, data["data"]):
        log = log.copy()
        log["embedding"] = embedding["embedding"]  # list of floats
        embeddings.append(log)
    return embeddings

# Example usage (will be removed in production)
if __name__ == "__main__":
    sample_logs = [
        {"timestamp": 1723732800, "message": "User successfully logged in"},
        {"timestamp": 1723732850, "message": "Failed authentication for user 123"}
    ]
    embedded = embed_log_messages(sample_logs)
    print("Embedded logs count:", len(embedded))
    for log in embedded:
        print(log["message"], ":", log["embedding"][:5], "...")  # show first few dims
