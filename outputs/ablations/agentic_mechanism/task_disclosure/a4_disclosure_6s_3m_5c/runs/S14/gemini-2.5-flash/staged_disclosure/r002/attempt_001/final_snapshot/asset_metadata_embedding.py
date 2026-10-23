
import openai
import os

def embed_metadata_and_text(metadata: dict, extracted_text: str) -> list[float]:
    """
    Embeds object metadata and extracted text using OpenAI's embedding API.

    Args:
        metadata (dict): A dictionary containing the object's metadata.
        extracted_text (str): The extracted text content of the object.

    Returns:
        list[float]: A list of floats representing the embedding vector.
    """
    # Ensure the OpenAI API key is set
    # It is recommended to load the API key from an environment variable
    # For example: os.environ.get("OPENAI_API_KEY")
    # For demonstration purposes, a placeholder is used here.
    # In a real application, you would load this securely.
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    # Combine metadata and extracted text into a single string for embedding
    # You might want to format this string more sophisticatedly depending on your needs
    combined_content = f"Metadata: {metadata}\nText: {extracted_text}"

    try:
        response = openai.embeddings.create(
            input=combined_content,
            model="text-embedding-ada-002"  # Concrete OpenAI model identifier
        )
        return response.data[0].embedding
    except openai.APIError as e:
        print(f"OpenAI API error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    sample_metadata = {
        "title": "Annual Report 2023",
        "author": "Acme Corp",
        "date": "2023-12-31"
    }
    sample_text = "This is the financial summary for the year 2023, showing significant growth..."

    try:
        embedding_vector = embed_metadata_and_text(sample_metadata, sample_text)
        print(f"Embedding vector (first 5 elements): {embedding_vector[:5]}")
        print(f"Embedding vector dimension: {len(embedding_vector)}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Failed to generate embedding: {e}")
