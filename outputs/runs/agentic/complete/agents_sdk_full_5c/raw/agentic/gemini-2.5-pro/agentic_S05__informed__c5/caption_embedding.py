import os
import cohere
from dotenv import load_dotenv

from speech_models import TextEmbedding

def embed_caption_chunk(caption_text: str) -> TextEmbedding | None:
    """
    Embeds a caption chunk for semantic meeting search using Cohere.

    Args:
        caption_text: The text of the caption chunk.

    Returns:
        A TextEmbedding object containing the original text and its vector,
        or None if an error occurs.
    """
    load_dotenv()
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        print("Error: COHERE_API_KEY environment variable not set.")
        return None
        
    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=[caption_text],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        
        embedding_vector = response.embeddings[0]
        
        return TextEmbedding(
            text=caption_text,
            embedding=embedding_vector
        )
    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return None
