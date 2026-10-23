import os
from typing import List, Dict, Any
import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_log_messages(messages: List[str], project_id: str, location: str = "us-central1") -> List[Dict[str, Any]]:
    """Embeds selected log messages for semantic retrieval using Vertex AI TextEmbeddingModel."""
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("text-embedding-004") # or text-embedding-gecko@001

    print(f"Embedding {len(messages)} log messages...")

    # The embedding API can handle multiple texts in one request
    embeddings = model.get_embeddings(messages)

    embedded_results = []
    for i, embedding in enumerate(embeddings):
        embedded_results.append({
            "original_message": messages[i],
            "embedding": embedding.values # The actual vector values
        })
    
    return embedded_results

if __name__ == '__main__':
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
        exit(1)

    log_messages_to_embed = [
        "Database connection failed unexpectedly.",
        "Failed to authenticate user: invalid password.",
        "Unable to reach external payment gateway for transaction processing.",
        "Error 500: Internal server error during API call.",
        "User login successful from IP 192.168.1.100."
    ]

    print("\n--- Log Message Embedding ---")
    embedded_logs = embed_log_messages(log_messages_to_embed, project_id)
    for res in embedded_logs:
        print(f"Original: '{res['original_message']}'")
        print(f"Embedding (first 5 values): {res['embedding'][:5]}... (total {len(res['embedding'])} dimensions)\n")

    # Example of comparing embeddings (simple dot product for similarity)
    if len(embedded_logs) >= 2:
        from numpy import dot
        embedding1 = embedded_logs[0]["embedding"]
        embedding2 = embedded_logs[1]["embedding"]
        embedding3 = embedded_logs[4]["embedding"]

        similarity1_2 = dot(embedding1, embedding2)
        similarity1_3 = dot(embedding1, embedding3)
        
        print(f"Similarity between '{embedded_logs[0]['original_message']}' and '{embedded_logs[1]['original_message']}': {similarity1_2:.4f}")
        print(f"Similarity between '{embedded_logs[0]['original_message']}' and '{embedded_logs[4]['original_message']}': {similarity1_3:.4f}")
        print("\n(Higher similarity indicates closer semantic meaning)")
