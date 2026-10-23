import os
import cohere
from speech_models import CaptionEmbedding

def embed_caption_chunk(text: str) -> CaptionEmbedding | None:
    """
    Embeds caption chunks for semantic meeting search using Cohere.
    """
    try:
        api_key = os.environ.get("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable not set.")
            
        co = cohere.Client(api_key)

        response = co.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_document" # Use 'search_document' for embeddings to be stored in a vector DB
        )

        if response.embeddings:
            # The result is a list of embeddings, one for each input text.
            # We sent one text, so we get the first element.
            embedding_vector = response.embeddings[0]
            return CaptionEmbedding(text=text, embedding=embedding_vector)
        
        return None

    except Exception as e:
        print(f"An error occurred during embedding: {e}")
        return None
