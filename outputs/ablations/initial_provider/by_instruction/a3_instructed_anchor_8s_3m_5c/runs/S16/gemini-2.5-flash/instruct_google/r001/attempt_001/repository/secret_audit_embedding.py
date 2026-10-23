from google.cloud import aiplatform
from security_models import AuditNote

def embed_audit_note(project_id: str, location: str, audit_note_content: str) -> list[float]:
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.get_publisher_model("google/text-embedding-004")
    try:
        # The predict method for embedding models usually takes a list of texts
        response = model.predict(instances=[{"text": audit_note_content}])
        # The embeddings are typically found in a 'predictions' field of the response
        if response and response.predictions:
            # Assuming the first prediction contains the embedding vector
            return response.predictions[0]
        else:
            return []
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []
