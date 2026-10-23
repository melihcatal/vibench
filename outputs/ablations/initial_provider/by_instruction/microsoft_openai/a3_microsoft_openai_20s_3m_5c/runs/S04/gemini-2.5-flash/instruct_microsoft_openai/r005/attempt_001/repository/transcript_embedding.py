import os
import openai
from typing import List, Optional

def embed_transcript_segments(text_segments: List[str], model_name: str = "text-embedding-ada-002") -> Optional[List[List[float]]]:
    """
    Embeds a list of text segments using OpenAI's embedding models for semantic retrieval.

    Args:
        text_segments: A list of strings, where each string is a segment to be embedded.
        model_name: The OpenAI embedding model to use (e.g., "text-embedding-ada-002").

    Returns:
        A list of embedding vectors (list of floats) for each text segment,
        or None if an error occurred.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    if not text_segments:
        return []

    try:
        print(f"Requesting embeddings from OpenAI using model: {model_name}...")
        # OpenAI's embedding API can take a list of texts in a single request
        response = openai.Embedding.create(
            input=text_segments,
            model=model_name
        )

        embeddings = [data.embedding for data in response.data]
        print("Embeddings generated successfully.")
        return embeddings

    except openai.error.OpenAIError as e:
        print(f"OpenAI API error during embedding: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during embedding: {e}")
        return None

if __name__ == "__main__":
    # Example Usage:
    # Set your OpenAI API key as an environment variable: export OPENAI_API_KEY="YOUR_API_KEY"

    # os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

    # if "OPENAI_API_KEY" in os.environ and os.environ["OPENAI_API_KEY"] != "YOUR_OPENAI_API_KEY":
    #     segments_to_embed = [
    #         "The cat sat on the mat.",
    #         "The dog chased the ball.",
    #         "Semantic search is powerful.",
    #         "Vector databases store embeddings."
    #     ]
    #     print(f"Embedding segments: {segments_to_embed}")
    #     
    #     embeddings = embed_transcript_segments(segments_to_embed)
    #     if embeddings:
    #         print(f"\nGenerated {len(embeddings)} embeddings. First embedding snippet (first 5 values):")
    #         if embeddings[0]:
    #             print(embeddings[0][:5]) # Print first 5 values of the first embedding
    #         print(f"Embedding dimension: {len(embeddings[0]) if embeddings else 0}")
    #     else:
    #         print("Failed to generate embeddings.")
    # else:
    #     print("Please set the OPENAI_API_KEY environment variable and uncomment the test lines.")
    print("To run this example, set OPENAI_API_KEY environment variable and uncomment the test lines.")
