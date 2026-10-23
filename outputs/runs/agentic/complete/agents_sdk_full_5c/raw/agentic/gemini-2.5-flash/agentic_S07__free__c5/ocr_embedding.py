import os
from typing import List
from google.cloud import aiplatform

# Initialize Vertex AI (assuming document_client handles actual init for production)
# aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location="us-central1")

def embed_text_sections(project_id: str, location: str, texts: List[str], model_name: str = "text-embedding-004") -> List[List[float]]:
    """Embeds extracted document sections for semantic retrieval using Google Cloud Vertex AI (Generative AI)."""
    aiplatform.init(project=project_id, location=location)

    # The Embedding Model is accessed differently than GenerativeModel.
    # It's usually through the aiplatform.gapic.PredictionServiceClient or a dedicated SDK method.
    # For now, we will use the preview SDK which simplifies this.
    embedding_model = aiplatform.LanguageModel.from_pretrained(model_name)

    # The `embed_text` method takes a list of texts
    try:
        response = embedding_model.embed_text(texts)
        # The response will contain a list of Embedding objects, each with a values attribute (list of floats)
        embeddings = [embedding.values for embedding in response.embeddings]
        return embeddings
    except Exception as e:
        print(f"Error embedding text: {e}")
        return []

if __name__ == '__main__':
    # Example usage
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # location = "us-central1" # Ensure your model is available in this region
    #
    # if project_id:
    #     document_sections = [
    #         "The quick brown fox jumps over the lazy dog.",
    #         "A fast, ginger-colored canid leaps above a sleepy canine.",
    #         "Neural networks are powerful tools for machine learning."
    #     ]
    #     embeddings = embed_text_sections(project_id, location, document_sections)
    #     for i, emb in enumerate(embeddings):
    #         print(f"Embedding for section {i+1} (first 5 values): {emb[:5]}...")
    #         print(f"  Dimension: {len(emb)}")
    # else:
    #     print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    pass
