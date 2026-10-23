import os
import cohere
from typing import List, Optional

def embed_caption_chunks(chunks: List[str]) -> Optional[List[List[float]]]:
    """
    Embeds caption chunks for semantic search using the Cohere API.

    Args:
        chunks: A list of text strings (caption chunks) to embed.

    Returns:
        A list of embedding vectors, or None if an error occurs.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        print("Error: COHERE_API_KEY environment variable not set.")
        return None
        
    try:
        co = cohere.Client(api_key)
        
        response = co.embed(
            texts=chunks,
            model='embed-english-v3.0',
            input_type='search_document'
        )
        
        return response.embeddings
        
    except Exception as e:
        print(f"An error occurred with the Cohere API: {e}")
        return None

if __name__ == '__main__':
    if "COHERE_API_KEY" in os.environ:
        caption_chunks_to_embed = [
            "The team discussed the quarterly budget results.",
            "Action item: Alice needs to follow up on the marketing campaign.",
            "There was a technical issue with the deployment pipeline.",
            "The meeting concluded with a plan for the next sprint."
        ]

        embeddings = embed_caption_chunks(caption_chunks_to_embed)

        if embeddings:
            print(f"Successfully generated {len(embeddings)} embeddings.")
            print("Dimension of the first embedding:", len(embeddings[0]))
            # print("First embedding vector (first 5 dimensions):", embeddings[0][:5])
    else:
        print("Please set the COHERE_API_KEY environment variable to run this example.")
