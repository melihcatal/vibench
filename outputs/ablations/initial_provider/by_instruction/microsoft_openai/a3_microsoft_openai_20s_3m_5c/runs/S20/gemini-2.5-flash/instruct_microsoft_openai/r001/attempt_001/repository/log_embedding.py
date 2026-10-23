import os
from typing import List
from observability_client import observability_client

def embed_log_messages(log_messages: List[str]) -> List[List[float]]:
    try:
        # Azure OpenAI Embeddings API
        response = observability_client.azure_openai_client.embeddings.create(
            input=log_messages,
            model=os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", "text-embedding-ada-002") # Example embedding model
        )
        
        embeddings = [data.embedding for data in response.data]
        
        print(f"Generated embeddings for {len(log_messages)} log messages.")
        # print(f"First embedding (truncated): {embeddings[0][:5]}...") # For brevity
        
        return embeddings

    except Exception as e:
        print(f"Error embedding log messages: {e}")
        return []

# Example usage (for testing purposes)
# if __name__ == "__main__":
#     sample_logs = [
#         "User login attempt failed from IP 192.168.1.10",
#         "Database connection established successfully on port 5432",
#         "Failed to authenticate user due to incorrect password"
#     ]
#     log_embeddings = embed_log_messages(sample_logs)
#     if log_embeddings:
#         print(f"Number of embeddings: {len(log_embeddings)}")
#         print(f"Dimension of each embedding: {len(log_embeddings[0])}")
