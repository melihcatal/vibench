import os
from observability_client import ObservabilityClient
from typing import List

def embed_log_messages(log_messages: List[str]):
    client = ObservabilityClient()
    
    if not client.openai_client:
        print("Azure OpenAI client not initialized. Cannot embed log messages.")
        return []
        
    embedding_deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", "text-embedding-ada-002")

    try:
        response = client.openai_client.embeddings.create(
            input=log_messages,
            model=embedding_deployment_name
        )
        
        embeddings = [data.embedding for data in response.data]
        
        return embeddings
        
    except Exception as e:
        print(f"Error embedding log messages with Azure OpenAI: {e}")
        return []