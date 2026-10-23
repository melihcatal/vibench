import os
import google.generativeai as genai


def get_gemini_embedding_model():
    """
    Provides a Google Gemini embedding model.
    Authenticates using GOOGLE_API_KEY environment variable.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.embed_content


def embed_asset_metadata_and_text(
    text_content: str,
    metadata: dict = None,
) -> list[float]:
    """
    Embeds object metadata and extracted text for search using Gemini embeddings.

    Args:
        text_content: The main text content to embed.
        metadata: Optional dictionary of metadata to include in the embedding.
                  The metadata values will be converted to strings and concatenated with the text_content.

    Returns:
        A list of floats representing the embedding vector.
    """
    embedding_model = get_gemini_embedding_model()

    combined_text = text_content
    if metadata:
        metadata_string = " ".join(f"{k}: {v}" for k, v in metadata.items())
        combined_text = f"{text_content} {metadata_string}"

    response = embedding_model(model="models/embedding-001", content=combined_text)

    return response["embedding"]
