import os
from openai import AzureOpenAI
from typing import List

def embed_document_sections(sections: List[str]) -> List[List[float]]:
    # Azure OpenAI API configuration for embeddings
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_key = os.environ.get("AZURE_OPENAI_KEY")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01") # e.g., "2024-02-01"
    embedding_deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME") # e.g., "text-embedding-ada-002"

    if not azure_endpoint or not api_key or not embedding_deployment_name:
        raise ValueError("AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, and AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME environment variables must be set for embeddings.")

    client = AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version
    )

    embeddings_list = []
    for text_section in sections:
        try:
            response = client.embeddings.create(
                input=text_section,
                model=embedding_deployment_name # Use your embedding deployment name
            )
            embeddings_list.append(response.data[0].embedding)
        except Exception as e:
            print(f"Error generating embedding for section: '{text_section[:50]}...' - {e}")
            embeddings_list.append([]) # Append an empty list or handle error as appropriate

    return embeddings_list
