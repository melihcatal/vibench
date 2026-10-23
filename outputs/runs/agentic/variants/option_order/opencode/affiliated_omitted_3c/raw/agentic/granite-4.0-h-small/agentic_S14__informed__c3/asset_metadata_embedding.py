# asset_metadata_embedding.py
import os
from google.cloud import storage
from google.cloud import generativeai as genai
from google.cloud import firebasedatabase  # placeholder for indexing, not used directly
from storage_client import get_client, bucket_name
from storage_models import normalize_object_name

SERVICE = "Google Gemini API"

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
embedding_model = genai.GenerativeModel("gemini-1.5-flash")


def embed_object_metadata(object_name: str) -> dict:
    """Create an embedding based on object metadata plus extracted text."""
    client = get_client()
    bucket = client.bucket(bucket_name())
    blob = bucket.blob(normalize_object_name(object_name))
    # Gather metadata
    metadata = {
        "name": blob.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "created": blob.time_created.isoformat(),
        "updated": blob.time_updated.isoformat(),
    }
    # Assume a function to fetch extracted text (e.g., from OCR)
    extracted_text = blob.download_as_text()  # simplistic approach
    prompt = f"Summarize the following object's metadata and content in a few sentences suitable for search:\\n\\nMetadata:\\n{metadata}\\n\\nContent preview (first 200 characters): {extracted_text[:200]}..."
    # Generate embedding using Gemini's text embedding capability
    response = embedding_model.embed_content(
        prompt,
        generation_config=genai.GenerativeModel.GenerationConfig(temperature=0.0),
    )
    return {
        "object_name": object_name,
        "embedding": response.embeddings[0].values,  # list of floats
    }


# Example of indexing the embedding (pseudo-code, would use Firebase or a vector DB)
def index_embedding(embedding_record: dict):
    # Placeholder - in production you'd push to a vector store like Vertex AI,
    # Pinecone, or a Firestore collection with the embedding vector.
    print("Would index embedding in vector DB...", embedding_record)

    # Sample usage\nif __name__ == "__main__":
    result = embed_object_metadata("example.pdf")
    print(result)
    index_embedding(result)
