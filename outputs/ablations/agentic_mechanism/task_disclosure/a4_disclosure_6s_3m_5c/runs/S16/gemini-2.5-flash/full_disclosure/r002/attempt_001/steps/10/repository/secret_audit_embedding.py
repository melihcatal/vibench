
import os
from google.cloud import aiplatform

def embed_secret_audit_notes(audit_notes: list[str]) -> list[list[float]]:
    """
    Embeds a list of secret audit notes using Google Cloud Vertex AI's text-bison model.

    Args:
        audit_notes: A list of strings, where each string is an audit note.

    Returns:
        A list of lists of floats, where each inner list is the embedding for an audit note.
    """
    aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_REGION"))

    model = aiplatform.get_model_matching_prefix("text-embedding-gecko@003") 
    
    embeddings = []
    for note in audit_notes:
        response = model.predict([note])
        embeddings.append(response.predictions[0].embeddings.values)
    return embeddings

