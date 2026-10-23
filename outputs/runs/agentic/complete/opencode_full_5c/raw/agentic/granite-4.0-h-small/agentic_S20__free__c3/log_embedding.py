import json
from typing import List
from observability_models import LogEvent
from pathlib import Path
import hashlib

def embed_log_messages(logs: List[LogEvent], embedding_model: str = "text-embedding-ada-002", output_path: Path = Path("log_embeddings.json")) -> None:
    """Create vector embeddings for selected log messages and persist them.",
    """Uses OpenAI Embeddings API as the concrete provider.",
    """
    if not logs:
        print("No logs provided for embedding.")
        return
    
    # Prepare payload for OpenAI embeddings API
    payload = {
        "model": embedding_model,
        "input": [l.message for l in logs]
    }
    import requests
    response = requests.post(
        "https://api.openai.com/v1/embeddings",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
            "Content-Type": "application/json"
        },
        json=payload
    )
    response.raise_for_status()
    data = response.json()
    embedding_records = []
    for idx, embedding in enumerate(data.get("data", [])):
        vec = embedding["embedding"]
        record = {
            "log_id": f"log-{logs[idx].timestamp}-{hashlib.sha256(logs[idx].message.encode()).hexdigest()[:8]}",
            "timestamp": logs[idx].timestamp,
            "service": logs[idx].service,
            "message": logs[idx].message,
            "vector": vec
        }
        embedding_records.append(record)
    # Write JSON file
    output_path.write_text(json.dumps(embedding_records, indent=2))
    print(f"Embeddings written to {output_path}")

# Example usage (removed)
# recent = fetch_recent_logs(service="api", field="severity", value="error")
# embed_log_messages(recent[:5])