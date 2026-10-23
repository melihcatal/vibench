import os
from openai import AzureOpenAI
from typing import Dict, Any


def get_embeddings(text_input: str) -> list[float]:
    azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_openai_key = os.getenv("AZURE_OPENAI_KEY")
    azure_openai_embedding_deployment_name = os.getenv(
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"
    )  # e.g., text-embedding-ada-002

    if (
        not azure_openai_endpoint
        or not azure_openai_key
        or not azure_openai_embedding_deployment_name
    ):
        raise ValueError(
            "AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, and AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME environment variables must be set."
        )

    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version="2024-02-15-preview",  # Use a compatible API version
    )

    try:
        response = client.embeddings.create(
            model=azure_openai_embedding_deployment_name,  # model = "deployment_name"
            input=[text_input],
        )
        return response.data[0].embedding
    except Exception as e:
        raise RuntimeError(f"Error generating embeddings: {e}")


def embed_asset_metadata_and_text(
    metadata: Dict[str, str], extracted_text: str
) -> Dict[str, list[float]]:
    # Combine metadata and extracted text into a single string for embedding
    metadata_string = " ".join(f"{k}: {v}" for k, v in metadata.items())
    combined_text = f"Metadata: {metadata_string}. Content: {extracted_text}"

    embedding = get_embeddings(combined_text)

    return {"combined_embedding": embedding}
