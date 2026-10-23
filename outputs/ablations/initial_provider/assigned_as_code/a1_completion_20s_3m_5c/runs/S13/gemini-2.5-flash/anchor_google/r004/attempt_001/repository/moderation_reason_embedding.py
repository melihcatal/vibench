import os
from google.cloud import aiplatform

def embed_moderation_reason(text, project_id=None, location=None):
    project_id = project_id or os.environ.get("GCP_PROJECT_ID")
    location = location or os.environ.get("GCP_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GCP_PROJECT_ID not found in config or environment variables.")

    aiplatform.init(project=project_id, location=location)

    # Using a text embedding model
    # The model name should be specific, e.g., 'text-embedding-004' or similar.
    # For this example, I'll use a generic embedding model.
    # The exact model ID might vary, referring to https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/text-embeddings
    # For example, 'text-embedding-gecko@001' or similar.
    try:
        model = aiplatform.Endpoint.from_pretrained("projects/{}/locations/{}/models/text-embedding-gecko@001".format(project_id, location))
    except Exception:
        model = aiplatform.Endpoint.from_pretrained("text-embedding-gecko") # Fallback to a generic name

    response = model.predict(prompt=text)
    # The structure of the response might vary based on the model and SDK version.
    # Assuming the embeddings are directly in predictions for simplicity.
    # It might be response.predictions[0]['embeddings'] or similar.
    # This is a placeholder, actual access needs to be verified with the real API response.
    if response.predictions and len(response.predictions) > 0:
        # Assuming the embedding is directly accessible from the prediction object for simplicity.
        # In a real scenario, you might need to parse `response.predictions[0]`
        # For text-embedding-gecko, the embeddings are usually in response.predictions[0]['embedding']
        return response.predictions[0]['embedding']
    return []
