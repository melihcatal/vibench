
from google.cloud import aiplatform

def embed_text(text: str) -> list[float]:
    """
    Embeds a given text using Google Cloud Vertex AI's TextEmbeddingModel.
    """
    # Initialize Vertex AI
    # Replace 'your-project-id' and 'your-location' with your actual GCP project ID and region.
    aiplatform.init(project="your-project-id", location="your-location")

    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values

if __name__ == "__main__":
    audit_note = "Discovered an unencrypted API key in the configuration file during the security audit."
    embedding = embed_text(audit_note)
    print(f"Embedding for the audit note (first 5 dimensions): {embedding[:5]}...")
