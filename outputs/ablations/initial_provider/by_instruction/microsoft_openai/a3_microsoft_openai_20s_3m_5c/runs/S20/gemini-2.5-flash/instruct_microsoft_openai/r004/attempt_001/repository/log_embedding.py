from observability_client import ObservabilityClient
from typing import List, Optional

def embed_log_messages(log_messages: List[str], model: str = "text-embedding-ada-002") -> Optional[List[List[float]]]:
    client = ObservabilityClient()
    openai_client = client.get_openai_client()

    if not openai_client:
        print("OpenAI client not configured. Cannot generate embeddings.")
        return None

    if not log_messages:
        return []

    try:
        response = openai_client.embeddings.create(
            input=log_messages,
            model=model
        )
        embeddings = [data.embedding for data in response.data]
        print(f"Generated {len(embeddings)} embeddings using model '{model}'.")
        return embeddings
    except Exception as e:
        print(f"An error occurred during embedding generation with OpenAI: {e}")
        return None

if __name__ == "__main__":
    # Example usage:
    messages_to_embed = [
        "User login successful from IP 192.168.1.1.",
        "Failed to connect to the database. Connection refused.",
        "New order created with ID ORD-123. Customer: Alice.",
        "Database connection failed. Check network configuration."
    ]

    embeddings = embed_log_messages(messages_to_embed)

    if embeddings:
        for i, emb in enumerate(embeddings):
            print(f"Embedding for '{messages_to_embed[i][:40]}...': {emb[:5]}... (length: {len(emb)})")

        # Example of how to use embeddings (e.g., for similarity search)
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np

        if len(embeddings) >= 2:
            # Convert to numpy arrays for similarity calculation
            np_embeddings = np.array(embeddings)

            # Calculate cosine similarity between the first two messages
            similarity_0_1 = cosine_similarity(np_embeddings[0].reshape(1, -1), np_embeddings[1].reshape(1, -1))[0][0]
            print(f"\nCosine similarity between msg 0 and msg 1: {similarity_0_1:.4f}")

            # Calculate cosine similarity between message 1 (db fail) and message 3 (db fail)
            similarity_1_3 = cosine_similarity(np_embeddings[1].reshape(1, -1), np_embeddings[3].reshape(1, -1))[0][0]
            print(f"Cosine similarity between msg 1 and msg 3: {similarity_1_3:.4f}")

            # Calculate cosine similarity between message 0 (login success) and message 2 (order created)
            similarity_0_2 = cosine_similarity(np_embeddings[0].reshape(1, -1), np_embeddings[2].reshape(1, -1))[0][0]
            print(f"Cosine similarity between msg 0 and msg 2: {similarity_0_2:.4f}")

