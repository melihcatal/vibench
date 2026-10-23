import os
from openai import AzureOpenAI
from typing import List

def get_transcript_embeddings(segments: List[str]) -> List[List[float]]:
    # Azure OpenAI credentials
    # Set these environment variables: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview") # Default to a recent version
    deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME") # e.g., text-embedding-ada-002

    if not azure_endpoint or not api_key or not deployment_name:
        raise ValueError("AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, and AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME environment variables must be set for Azure OpenAI Embeddings.")

    try:
        client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            api_key=api_key,
            api_version=api_version
        )

        # Azure OpenAI embeddings API takes a list of strings
        response = client.embeddings.create(
            model=deployment_name, # This is the deployment name for your embeddings model
            input=segments
        )

        embeddings = [item.embedding for item in response.data]
        return embeddings

    except Exception as e:
        print(f"Error getting transcript embeddings with Azure OpenAI: {e}")
        return []

if __name__ == '__main__':
    # Example usage
    # sample_segments = [
    #     "The cat sat on the mat.",
    #     "The dog chased the ball.",
    #     "Artificial intelligence is transforming industries."
    # ]
    # embeddings_list = get_transcript_embeddings(sample_segments)
    # if embeddings_list:
    #     for i, embedding in enumerate(embeddings_list):
    #         print(f"Embedding for segment {i+1} (first 5 dims): {embedding[:5]}...")
    #         print(f"Length of embedding: {len(embedding)}")
    # else:
    #     print("Failed to retrieve embeddings.")
    pass
