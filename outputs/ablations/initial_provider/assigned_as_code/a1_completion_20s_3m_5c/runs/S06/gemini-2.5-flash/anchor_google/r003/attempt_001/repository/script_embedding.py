from google.cloud import aiplatform
import os

def embed_script(text, project_id=None, location="us-central1"):
    if project_id is None:
        # Attempt to get project ID from environment variable or gcloud config
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud project ID not found. Please set GOOGLE_CLOUD_PROJECT environment variable or pass it directly.")

    aiplatform.init(project=project_id, location=location)
    
    # Use the pre-trained text embedding model
    # You might need to specify a more precise model_id depending on the available models
    # For example, "text-embedding-004" or similar if available and suitable.
    # For this example, I'll use a generic reference as specific model IDs can change.
    # In a real scenario, you'd confirm the exact model ID from Vertex AI documentation.
    model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko@003") # A common, general-purpose embedding model

    embeddings = model.get_embeddings([text])
    
    # The embeddings object is a list of Embedding objects, each with values (list of floats)
    if embeddings and embeddings[0].values:
        return {"embedding": embeddings[0].values}
    else:
        return {"embedding": []}
