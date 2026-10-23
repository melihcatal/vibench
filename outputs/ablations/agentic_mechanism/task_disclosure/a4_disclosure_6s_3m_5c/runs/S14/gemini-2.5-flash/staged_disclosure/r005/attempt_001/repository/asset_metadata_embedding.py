
import os
from openai import OpenAI

# Initialize the OpenAI client
# Make sure to set your OpenAI API key as an environment variable (OPENAI_API_KEY)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def embed_text(text: str) -> list[float]:
    """
    Embeds a given text using OpenAI's embedding model.
    
    Args:
        text: The input text to embed.
        
    Returns:
        A list of floats representing the embedding vector.
    """
    if not client.api_key:
        raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"  # Concrete OpenAI model identifier
    )
    return response.data[0].embedding

def embed_metadata_and_text(metadata: dict, extracted_text: str) -> dict:
    """
    Embeds object metadata and extracted text for search purposes.
    
    Args:
        metadata: A dictionary containing the object's metadata.
        extracted_text: The extracted text content of the object.
        
    Returns:
        A dictionary containing the original metadata, extracted text, and their embeddings.
    """
    metadata_string = " ".join(f"{k}: {v}" for k, v in metadata.items())
    combined_text = f"{metadata_string} {extracted_text}"
    
    embedding = embed_text(combined_text)
    
    return {
        "metadata": metadata,
        "extracted_text": extracted_text,
        "embedding": embedding
    }
