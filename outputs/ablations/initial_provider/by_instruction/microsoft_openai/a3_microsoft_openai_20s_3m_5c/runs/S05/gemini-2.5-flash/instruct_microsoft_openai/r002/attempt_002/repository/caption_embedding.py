import asyncio
import os
from typing import List
from google.cloud import aiplatform
from speech_models import LiveCaption

async def embed_caption_chunks(caption_chunks: List[LiveCaption]) -> List[List[float]]:
    """Embeds caption chunks for semantic meeting search using Google Cloud Vertex AI Embeddings."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") # e.g., "your-gcp-project-id"
    location = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1") # e.g., "us-central1"

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    aiplatform.init(project=project_id, location=location)

    # Use the text-embedding-004 model for embeddings
    # Or other suitable models like 'text-embedding-gecko@003'
    model = aiplatform.get_model("text-embedding-004")

    texts_to_embed = [chunk.text for chunk in caption_chunks]

    if not texts_to_embed:
        return []

    print(f"Creating embeddings for {len(texts_to_embed)} caption chunks...")
    try:
        # The predict method returns a list of EndpointResponse objects, each containing an embedding.
        # We extract the embeddings (list of floats) from these responses.
        embeddings = model.predict(texts_to_embed).embeddings
        embedding_vectors = [embedding.values for embedding in embeddings]

        print(f"Generated {len(embedding_vectors)} embeddings.")
        return embedding_vectors
    except Exception as e:
        print(f"Error creating embeddings with Vertex AI: {e}")
        return []

async def main():
    # Set your Google Cloud project and region environment variables
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"
    # os.environ["GOOGLE_CLOUD_REGION"] = "us-central1"
    # Ensure you have authenticated to Google Cloud (e.g., gcloud auth application-default login)

    print("Creating embeddings for example caption chunks...")
    example_chunks = [
        LiveCaption(text="The sales team discussed new strategies.", language="en", is_partial=False),
        LiveCaption(text="Marketing presented their Q4 plan and budget.", language="en", is_partial=False),
        LiveCaption(text="Customer feedback highlighted a need for feature improvements.", language="en", is_partial=False)
    ]

    embeddings = await embed_caption_chunks(example_chunks)
    for i, emb in enumerate(embeddings):
        print(f"Embedding for chunk {i}: {emb[:5]}... (truncated)") # Print first 5 dimensions

if __name__ == "__main__":
    asyncio.run(main())
