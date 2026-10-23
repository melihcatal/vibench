import os
from openai import OpenAI
from typing import List

def get_caption_embedding(text: str) -> List[float]:
    # Use Azure OpenAI if AZURE_OPENAI_ENDPOINT is set, otherwise use OpenAI
    if os.environ.get("AZURE_OPENAI_ENDPOINT"):
        client = OpenAI(
            azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT"), 
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),  
            api_version="2024-02-01" # or your specific API version
        )
        model_deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", "text-embedding-ada-002") # e.g., your embedding deployment name
    else:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        model_deployment_name = "text-embedding-ada-002"

    if not client.api_key:
        raise ValueError("OPENAI_API_KEY or AZURE_OPENAI_API_KEY must be set.")

    try:
        response = client.embeddings.create(
            input=text,
            model=model_deployment_name # Model family: text-embedding-ada-002
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting caption embedding: {e}")
        return []

# Example usage (for integration test):
# if __name__ == "__main__":
#     os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
#     # Or for Azure OpenAI:
#     # os.environ["AZURE_OPENAI_ENDPOINT"] = "https://YOUR_AOAI_RESOURCE_NAME.openai.azure.com/"
#     # os.environ["AZURE_OPENAI_API_KEY"] = "YOUR_AOAI_KEY"
#     # os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"] = "YOUR_EMBEDDING_DEPLOYMENT_NAME"
#     embedding = get_caption_embedding("The quick brown fox jumps over the lazy dog.")
#     print(f"Embedding length: {len(embedding)}")
#     print(f"First 5 embedding values: {embedding[:5]}")
