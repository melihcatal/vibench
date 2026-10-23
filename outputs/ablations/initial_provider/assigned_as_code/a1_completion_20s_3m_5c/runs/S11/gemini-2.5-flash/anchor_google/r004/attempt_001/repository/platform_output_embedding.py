from google.cloud import aiplatform
from model_models import ModelResponse

def platform_output_embedding(model_response: ModelResponse):
    project_id = model_response.metadata.get("project_id")
    location = model_response.metadata.get("location")

    if not project_id or not location:
        raise ValueError("Project ID and location not found in model response metadata.")

    aiplatform.init(project=project_id, location=location)

    # Using a common embedding model provided by Vertex AI
    # The exact model name might vary, so it's good practice to make it configurable
    embedding_model_name = "text-embedding-004" # or "text-embedding-gecko@003"
    model = aiplatform.TextEmbeddingModel.from_pretrained(embedding_model_name)

    embeddings = model.predict([model_response.text])

    # The embeddings.predictions will contain a list of Embedding objects
    # Each Embedding object has a .values attribute which is the list of floats
    embedding_values = [e.values for e in embeddings.predictions]

    return {"text": model_response.text, "embedding": embedding_values}
