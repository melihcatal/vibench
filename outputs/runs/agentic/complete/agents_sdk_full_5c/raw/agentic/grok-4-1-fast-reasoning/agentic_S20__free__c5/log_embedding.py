import os
from openai import OpenAI
import json

SAMPLE_LOGS = ["Payment processing error", "Successful deployment to prod", "User login failed"]

def generate_log_embeddings(logs: list[str]):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=logs
    )
    embeddings = [emb.embedding for emb in response.data]
    print(json.dumps({
        "num_logs": len(embeddings),
        "embedding_dim": len(embeddings[0]) if embeddings else 0
    }))
    return embeddings

if __name__ == "__main__":
    generate_log_embeddings(SAMPLE_LOGS)