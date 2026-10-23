import openai
import os
import json

def embed_asset_metadata(metadata: dict, extracted_text: str) -> list[float]:
    """
    Embeds object metadata and extracted text for search using OpenAI embeddings.

    Args:
        metadata: A dictionary containing the object's metadata.
        extracted_text: The extracted text content from the object.

    Returns:
        A list of floats representing the embedding vector.
    """
    # Initialize OpenAI client with API key from environment variable
    # This makes OpenAI the concrete external provider, identifiable by 'openai.OpenAI' and model name.
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Combine metadata and extracted text into a single string for embedding
    metadata_string = json.dumps(metadata, sort_keys=True)
    combined_text = f"Metadata: {metadata_string}\n\nContent: {extracted_text}"

    # Create embedding using OpenAI's text-embedding-ada-002 model
    response = client.embeddings.create(
        input=combined_text,
        model="text-embedding-ada-002"  # Concrete model identifier
    )
    return response.data[0].embedding

