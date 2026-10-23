from google.cloud import aiplatform
from security_models import CryptoAuditEmbeddingRequest, CryptoAuditEmbeddingResponse
import os
import json # For serializing log_entry to string

def embed_crypto_audit_notes(request: CryptoAuditEmbeddingRequest) -> CryptoAuditEmbeddingResponse:
    """
    Embeds crypto audit notes for semantic search using Google Cloud Vertex AI Embeddings.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT_ID environment variable not set. Using 'your-gcp-project-id'.")
        project_id = "your-gcp-project-id"

    location = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1") # Default to us-central1
    
    aiplatform.init(project=project_id, location=location)

    # Use a text embedding model (e.g., "textembedding-gecko@001")
    # The model name might vary, choose an appropriate one.
    # For production, consider deploying a specific version or using a stable model ID.
    model_name = "textembedding-gecko@001"
    embeddings_model = aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})

    # The audit log entry needs to be converted to a string for embedding.
    # We can serialize the dictionary to a JSON string.
    text_to_embed = json.dumps(request.log_entry, sort_keys=True)

    instances = [
        {"content": text_to_embed}
    ]
    
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_name}"

    try:
        response = embeddings_model.predict(endpoint=endpoint, instances=instances)
        # Assuming the response structure for textembedding-gecko@001,
        # where embeddings are in predictions[0]['embeddings']['values']
        embedding_values = response.predictions[0]["embeddings"]["values"]
        return CryptoAuditEmbeddingResponse(embedding=list(embedding_values))
    except Exception as e:
        print(f"Error generating embedding: {e}")
        # Return an empty embedding or raise an error based on desired behavior
        return CryptoAuditEmbeddingResponse(embedding=[])

import os
import json
