from google.cloud import aiplatform
from security_client import get_gcp_project_id
from security_models import CryptoAuditNote
from typing import List
import os

def embed_audit_notes(project_id: str, location: str, notes: List[CryptoAuditNote]) -> List[List[float]]:
    """Embeds crypto audit notes using Google Cloud Vertex AI (text-embedding-004).

    Args:
        project_id: The GCP project ID.
        location: The GCP region where Vertex AI is enabled (e.g., "us-central1").
        notes: A list of CryptoAuditNote objects to embed.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    aiplatform.init(project=project_id, location=location)

    # Use the text-embedding-004 model
    # Model details: https://cloud.google.com/vertex-ai/docs/generative/text-embeddings/retrieve-text-embeddings
    model_name = "text-embedding-004"
    try:
        model = aiplatform.get_model_registry().get_model(model_name)
        embedding_model = model.version_aliases["latest"].get_version_id()
        
        # Prepare instances for the prediction endpoint
        instances = [{'text_content': note.note_text} for note in notes]

        # Create an embedding client (this implicitly uses the configured project/location)
        embed_client = aiplatform.gapic.PredictionServiceClient(client_options={
            'api_endpoint': f"{location}-aiplatform.googleapis.com"
        })
        
        endpoint_name = embed_client.endpoint_path(project_id, location, "text-embedding-gecko-001") # Or a specific endpoint if deployed custom
        # The `text-embedding-004` model is generally accessed via a common endpoint for base models.
        # If there's no specific deployed endpoint for 'text-embedding-004', this might need adjustment to a gen-ai specific method or model id.
        # For now, using get_model and then assuming a prediction call. 
        # A more direct route might be through `vertexai.preview.language_models.TextEmbeddingModel.from_pretrained("text-embedding-004")`
        # or directly calling the generative AI API.

        # Let's use the direct TextEmbeddingModel for better clarity with gen-AI models.
        from vertexai.language_models import TextEmbeddingModel
        embedding_model = TextEmbeddingModel.from_pretrained("text-embedding-004")

        text_to_embed = [note.note_text for note in notes]
        embeddings = embedding_model.get_embeddings(text_to_embed)

        return [embedding.values for embedding in embeddings]

    except Exception as e:
        print(f"Error embedding audit notes: {e}")
        return []

if __name__ == '__main__':
    PROJECT_ID = get_gcp_project_id() # Ensure GOOGLE_CLOUD_PROJECT env var is set
    LOCATION = "us-central1" # Choose an appropriate Vertex AI region

    audit_notes = [
        CryptoAuditNote(id="1", timestamp="2023-01-01T10:00:00Z", note_text="Key 'key-prod-us' used for encryption of customer data in region 'us-east1'. Compliance check initiated.", key_id="key-prod-us", operation="Encrypt"),
        CryptoAuditNote(id="2", timestamp="2023-01-01T10:15:00Z", note_text="Decryption operation failed for 'key-dev-eu'. Investigating access permissions. User 'dev-team-a'.", key_id="key-dev-eu", operation="Decrypt"),
        CryptoAuditNote(id="3", timestamp="2023-01-02T11:00:00Z", note_text="New key 'key-prod-asia' rotated. Old key archived as per policy 'PCI-DSS-v4'.", key_id="key-prod-asia", operation="KeyRotation"),
        CryptoAuditNote(id="4", timestamp="2023-01-02T11:30:00Z", note_text="Customer data encryption performed with AES-256 using key 'key-prod-us'. Verified against security policy.", key_id="key-prod-us", operation="Encrypt"),
    ]

    print(f"Embedding {len(audit_notes)} audit notes in project {PROJECT_ID} in {LOCATION}...")
    try:
        embeddings = embed_audit_notes(PROJECT_ID, LOCATION, audit_notes)
        if embeddings:
            print(f"Generated {len(embeddings)} embeddings, each with dimension {len(embeddings[0])}.")
            # print("First embedding sample:", embeddings[0][:5], "...")
        else:
            print("No embeddings generated.")
    except Exception as e:
        print(f"Failed to generate embeddings: {e}")
