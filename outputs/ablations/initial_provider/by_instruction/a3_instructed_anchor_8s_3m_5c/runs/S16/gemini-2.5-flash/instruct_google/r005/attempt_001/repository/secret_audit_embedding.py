from google.cloud import aiplatform
from typing import List

def embed_text_with_vertex_ai(project_id: str, location: str, texts: List[str]) -> List[List[float]]:
    """
    Embeds a list of texts using Google Cloud Vertex AI's text-bison-001 model for semantic search.
    """
    aiplatform.init(project=project_id, location=location)
    
    # The embedding model to use. You might need to adjust this based on available models in your region.
    # Common models include 'text-embedding-004' or specific versions like 'text-bison@001'
    model = aiplatform.get_model_deployment("text-embedding-gecko@001") # Using a general purpose embedding model

    embeddings = []
    for text in texts:
        response = model.predict(instances=[{"content": text}])
        # Assuming the response structure contains an embedding for each instance
        # The exact field might vary based on the model version and API response format.
        # This is a common structure for text embedding responses.
        if response.predictions and len(response.predictions) > 0:
            # Access the embedding value from the prediction
            embedding_values = response.predictions[0]
            embeddings.append(embedding_values)
        else:
            embeddings.append([]) # Append an empty list if no embedding is found
            
    return embeddings

def embed_secret_audit_notes(project_id: str, location: str, audit_notes: List[str]) -> List[List[float]]:
    """
    Embeds secret audit notes for semantic search using Vertex AI.
    """
    if not audit_notes:
        return []
    return embed_text_with_vertex_ai(project_id, location, audit_notes)

if __name__ == "__main__":
    # Example usage:
    # project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    # location = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
    # example_notes = [
    #     "Secret for payment gateway updated due to expiry.",
    #     "Database credentials rotated as per quarterly policy.",
    #     "New API key generated for third-party integration."
    # ]
    # if project_id:
    #     embeddings = embed_secret_audit_notes(project_id, location, example_notes)
    #     for i, embedding in enumerate(embeddings):
    #         print(f"Embedding for note '{example_notes[i]}': {embedding[:5]}...") # Print first 5 dimensions
    # else:
    #     print("Please set GOOGLE_CLOUD_PROJECT environment variable.")
    pass
