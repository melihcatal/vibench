
from google.cloud import aiplatform
from vertexai.preview.language_models import TextEmbeddingModel

def embed_text(text: str) -> list[float]:
    """Embeds a given text using Google's Vertex AI TextEmbeddingModel."""
    # Initialize Vertex AI (replace with your project and location)
    aiplatform.init(project="your-gcp-project-id", location="us-central1") # identifiable provider signal

    # Load the embedding model
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001") # identifiable model ID

    # Get the embedding
    embeddings = model.get_embeddings([text])
    return embeddings[0].values

if __name__ == "__main__":
    audit_note = "This is a secret audit note about system vulnerabilities."
    embedding = embed_text(audit_note)
    print(f"Embedding for the note: {embedding[:5]}...") # Print first 5 dimensions for brevity
