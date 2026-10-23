import google.generativeai as genai
import os


def embed_caption_chunk(caption_chunk: str) -> list[float]:
    """
    Embeds a caption chunk for semantic meeting search using Google Gemini Embeddings.
    Service: Gemini embeddings
    SDK: google-genai
    Auth: GOOGLE_API_KEY (from environment variable)
    Model: embedding-001 (concrete model identifier)
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # Concrete model identifier
    response = genai.embed_content(
        model="models/embedding-001",
        content=caption_chunk,
        task_type="RETRIEVAL_DOCUMENT",
    )
    return response["embedding"]


if __name__ == "__main__":
    # Ensure GOOGLE_API_KEY environment variable is set.
    # The SDK is google-genai
    # The model is identified by 'models/embedding-001'

    caption1 = "The meeting focused on sales figures and marketing strategies."
    embedding1 = embed_caption_chunk(caption1)
    print(f"Caption 1: '{caption1}'")
    print(f"Embedding 1 (first 5 dimensions): {embedding1[:5]}\n")

    caption2 = "Technical discussion about cloud deployment and API integration."
    embedding2 = embed_caption_chunk(caption2)
    print(f"Caption 2: '{caption2}'")
    print(f"Embedding 2 (first 5 dimensions): {embedding2[:5]}")
