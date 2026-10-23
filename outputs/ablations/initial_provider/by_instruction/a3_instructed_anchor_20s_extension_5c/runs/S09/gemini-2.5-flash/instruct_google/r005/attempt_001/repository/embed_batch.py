import google.generativeai as genai
import os

def embed_batch(texts: list[str]) -> list[list[float]]:
    """Generates embedding vectors for a batch of text strings using Google's Generative AI.

    Args:
        texts: A list of input text strings.

    Returns:
        A list of lists of floats, where each inner list is an embedding vector for a corresponding text.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.get_model("models/embedding-001")
    response = model.embed_content(content=texts)
    return [item["embedding"] for item in response["embeddings"]]
