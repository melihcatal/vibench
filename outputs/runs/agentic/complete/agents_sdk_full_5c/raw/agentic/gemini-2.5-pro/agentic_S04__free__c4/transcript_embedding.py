import os
import voyageai
from typing import List


def embed_transcript_segments(segments: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of transcript segments using Voyage AI.

    Args:
        segments: A list of text strings (e.g., sentences or paragraphs).

    Returns:
        A list of embedding vectors, where each vector corresponds to a segment.
    """
    api_key = os.getenv("VOYAGE_API_KEY")
    if not api_key:
        raise ValueError("VOYAGE_API_KEY environment variable not set.")

    vo = voyageai.Client(api_key=api_key)

    # Using a model specialized for retrieval tasks.
    model_name = "voyage-2"

    result = vo.embed(texts=segments, model=model_name, input_type="document")

    return result.embeddings


# Example usage:
# if __name__ == '__main__':
#     transcript_chunks = [
#         "The board approved the new budget for the fiscal year.",
#         "Marketing will receive a 10% increase in funding.",
#         "Key initiatives include international expansion and product diversification.",
#         "The engineering team is focusing on improving system reliability.",
#     ]
#     embeddings = embed_transcript_segments(transcript_chunks)
#     print(f"Generated {len(embeddings)} embeddings.")
#     print(f"Dimension of the first embedding: {len(embeddings[0])}")
#     # print("First embedding vector (first 5 dimensions):", embeddings[0][:5])
