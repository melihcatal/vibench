import os
import cohere
from typing import List

def embed_transcript_segments(segments: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of transcript segments using Cohere.

    Args:
        segments: A list of strings (transcript segments) to embed.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    try:
        response = co.embed(
            texts=segments,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except cohere.CohereError as e:
        print(f"An error occurred with the Cohere API: {e}")
        return []

if __name__ == '__main__':
    transcript_segments = [
        "The main topic today is the Q3 marketing campaign.",
        "We need to finalize the budget by the end of the week.",
        "Projected ad spend is too high, we must reduce it by 15%.",
        "John will take the lead on revising the content creation budget.",
        "A revised plan will be ready by end of day Friday."
    ]
    
    embeddings = embed_transcript_segments(transcript_segments)

    if embeddings:
        print(f"Successfully generated {len(embeddings)} embeddings.")
        print("Dimension of the first embedding:", len(embeddings[0]))
        # print("First embedding (first 5 values):", embeddings[0][:5])
    else:
        print("Failed to generate embeddings.")
