import os
import vertexai
from vertexai.preview.language_models import TextEmbeddingModel
from typing import List

def embed_secret_audit_notes(project_id: str, location: str, notes: List[str]) -> List[List[float]]:
    """
    Embeds secret audit notes for semantic search using Google Cloud Vertex AI's Text Embedding model.
    Model: 'textembedding-gecko'
    """
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko")

    # The model can handle multiple texts in a single request.
    embeddings = model.get_embeddings(notes)
    
    # Extract the values from the Embedding objects
    return [embedding.values for embedding in embeddings]

if __name__ == "__main__":
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_REGION", "us-central1") # Or choose an appropriate region

    if project_id and location:
        audit_notes_to_embed = [
            "Secret password for 'admin' user was updated today after a suspected compromise.",
            "Database connection string rotated as part of monthly security hygiene.",
            "API key for external service X was revoked and a new one generated.",
            "Internal microservice secret changed due to service account credential update.",
            "Urgent rotation of sensitive financial system secret due to breach notification."
        ]
        try:
            print(f"Generating embeddings for {len(audit_notes_to_embed)} audit notes in project {project_id} at {location}...")
            embeddings_list = embed_secret_audit_notes(project_id, location, audit_notes_to_embed)

            if embeddings_list:
                for i, embedding in enumerate(embeddings_list):
                    print(f"Note {i+1} embedding (first 5 values): {embedding[:5]}...")
                print(f"Total embeddings generated: {len(embeddings_list)}")
                print(f"Dimension of each embedding: {len(embeddings_list[0])}")
            else:
                print("No embeddings generated.")

        except Exception as e:
            print(f"Error generating embeddings: {e}")
            print("Please ensure Vertex AI API is enabled and you have sufficient permissions.")
    else:
        print("GCP_PROJECT_ID and/or GCP_REGION environment variables not set.")
