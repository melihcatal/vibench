import asyncio
from google.cloud import aiplatform
import os
from typing import List, Dict, Any

# Initialize Vertex AI (replace with your project and location)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

try:
    aiplatform.init(project=PROJECT_ID, location=LOCATION)
except RuntimeError as e:
    if "Vertex AI SDK has already been initialized" in str(e):
        pass # Already initialized, safe to ignore
    else:
        raise

async def embed_caption_chunks(caption_chunk_async_generator, model_name="text-embedding-004"):
    """
    Embeds caption chunks for semantic meeting search using Google Cloud Vertex AI's TextEmbeddingModel.

    Args:
        caption_chunk_async_generator: An async generator that yields caption strings.
        model_name (str): The name of the Vertex AI embedding model to use (e.g., "text-embedding-004").

    Yields:
        A dictionary containing the original chunk and its embedding vector.
    """
    try:
        # Load the embedding model. This often involves a synchronous call.
        # aiplatform.TextEmbeddingModel.from_pretrained() is generally a synchronous operation.
        model = aiplatform.TextEmbeddingModel.from_pretrained(model_name)
    except Exception as e:
        print(f"Error loading Vertex AI TextEmbeddingModel '{model_name}': {e}")
        return

    print(f"Generating embeddings for caption chunks using Vertex AI model: {model_name}...")

    async for chunk in caption_chunk_async_generator:
        if not chunk.strip():
            continue

        try:
            # The predict method of the embedding model is often synchronous.
            # Use asyncio.to_thread to run it without blocking the event loop.
            embeddings_obj = await asyncio.to_thread(model.predict, [chunk])
            
            # The structure of embeddings_obj can vary. For text-embedding-004, it typically
            # returns a list of Embeddings objects, each with a values attribute (list of floats).
            if embeddings_obj and embeddings_obj.embeddings:
                embedding_vector = embeddings_obj.embeddings[0].values
                yield {"original_chunk": chunk, "embedding": embedding_vector}
            else:
                yield {"original_chunk": chunk, "embedding": []}
        except Exception as e:
            print(f"Error generating embedding: {e}")
            yield {"original_chunk": chunk, "embedding": f"Error: {e}"}

if __name__ == "__main__":
    async def mock_caption_chunks():
        yield "Meeting minutes for the Q4 financial review."
        await asyncio.sleep(1)
        yield "Discussion about new marketing strategies for product launch."
        await asyncio.sleep(1)
        yield "Action items from the project management stand-up."

    async def main():
        print("Starting caption embedding generation...")
        async for result in embed_caption_chunks(mock_caption_chunks()):
            print(f"Original Chunk: {result["original_chunk"]}")
            print(f"Embedding (first 5 values): {result["embedding"][:5]}...")
            print(f"Embedding Dimension: {len(result["embedding"]) if isinstance(result["embedding"], list) else 'N/A'}\n")

    asyncio.run(main())
