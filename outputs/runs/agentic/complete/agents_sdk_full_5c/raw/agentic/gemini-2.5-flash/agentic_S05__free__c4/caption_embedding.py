from google.cloud import aiplatform
import os
import numpy as np

def get_text_embedding_vertex_ai(
    text: str,
    project_id: str,
    location: str = "us-central1",
    model_id: str = "text-embedding-gecko@001", # Concrete model identifier for embeddings
) -> list[float]:
    """
    Gets text embeddings using a Google Cloud Vertex AI embedding model.

    Args:
        text: The text content to embed.
        project_id: The Google Cloud project ID.
        location: The Vertex AI endpoint location.
        model_id: The specific model ID for text embeddings (e.g., "text-embedding-gecko@001").

    Returns:
        A list of floats representing the embedding vector.
    """
    aiplatform.init(project=project_id, location=location)

    from vertexai.preview.language_models import TextEmbeddingModel

    model = TextEmbeddingModel.from_pretrained(model_id)

    embeddings = model.get_embeddings([text])
    # Each input text generates one embedding, so we take the first one.
    return embeddings[0].values

async def embed_caption_chunks(caption_stream_gen, project_id: str):
    """
    Embeds live caption chunks for semantic search.

    Args:
        caption_stream_gen: An async generator yielding (transcript, is_final) tuples.
        project_id: Your Google Cloud project ID.

    Yields:
        Tuples of (transcript, is_final, embedding_vector) for each final caption chunk.
    """
    async for transcript, is_final in caption_stream_gen:
        if transcript.strip() and is_final:
            embedding = get_text_embedding_vertex_ai(
                text=transcript,
                project_id=project_id,
            )
            yield transcript, is_final, embedding
        else:
            # For non-final or empty transcripts, yield no embedding or an empty one
            yield transcript, is_final, []

if __name__ == '__main__':
    # Example usage:
    # import asyncio
    #
    # GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    #
    # async def dummy_caption_source():
    #     yield "The quick brown fox jumps over the lazy dog.", True
    #     await asyncio.sleep(0.5)
    #     yield "How to quickly jump over obstacles?", True
    #     await asyncio.sleep(0.5)
    #     yield "This is a partial result.", False # Should not be embedded
    #
    # async def main():
    #     print(f"Generating embeddings for captions for project {GOOGLE_CLOUD_PROJECT}...")
    #     async for transcript, is_final, embedding in embed_caption_chunks(
    #         dummy_caption_source(), GOOGLE_CLOUD_PROJECT
    #     ):
    #         if is_final and embedding:
    #             print(f"Caption: \"{transcript}\"\nEmbedding (first 5 values): {embedding[:5]}...")
    #         else:
    #             print(f"Caption: \"{transcript}\" (Not embedded or partial)")
    #
    # if GOOGLE_CLOUD_PROJECT == "your-gcp-project-id":
    #     print("Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id'.")
    # else:
    #     asyncio.run(main())
    pass
