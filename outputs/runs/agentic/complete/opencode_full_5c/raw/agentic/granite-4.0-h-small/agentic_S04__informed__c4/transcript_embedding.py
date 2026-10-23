import os
from embedding_client import EmbeddingClient
import json


# Later-step: Embed transcript segments for semantic retrieval
def transcript_embedding(job_id):
    client = EmbeddingClient()
    transcript = client.fetch_transcript(job_id)
    # Split into manageable chunks (e.g., 500 characters)
    chunks = [transcript[i : i + 500] for i in range(0, len(transcript), 500)]
    embeddings = []
    for chunk in chunks:
        emb = client.embed_text(text=chunk)
        embeddings.append({"chunk": chunk, "embedding": emb})
    # Return JSON list of embeddings
    return json.dumps(embeddings)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: transcript_embedding.py <job_id>")
        sys.exit(1)
    job_id = sys.argv[1]
    embeddings_json = transcript_embedding(job_id)
    print("Embeddings:")
    print(embeddings_json)
