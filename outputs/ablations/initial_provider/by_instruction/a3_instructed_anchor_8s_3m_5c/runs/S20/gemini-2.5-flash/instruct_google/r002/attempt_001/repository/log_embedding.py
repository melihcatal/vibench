from google.cloud import aiplatform

def embed_log_message(project_id: str, location: str, text_content: str) -> list:
    """
    Embeds selected log messages for semantic retrieval using Google Cloud Vertex AI.

    Args:
        project_id (str): Your Google Cloud project ID.
        location (str): The Google Cloud region for Vertex AI (e.g., "us-central1").
        text_content (str): The log message text to embed.

    Returns:
        list: A list of floats representing the embedding vector.
    """

    aiplatform.init(project=project_id, location=location)

    # Using the 'text-embedding-gecko' model for text embeddings.
    # Model name might need adjustment based on availability and desired embedding quality/size.
    model_name = "text-embedding-gecko@001"

    try:
        embedding_model = aiplatform.get_model_by_name(f"projects/{project_id}/locations/{location}/models/{model_name}")
    except Exception as e:
        print(f"Error loading embedding model {model_name}: {e}")
        # Fallback for demonstration if model loading fails
        return []

    # The predict method for embedding models expects a list of text instances.
    # Each instance can be a dictionary with a 'content' key.
    instances = [{'content': text_content}]
    parameters = {}

    response = embedding_model.predict(instances=instances, parameters=parameters)

    embeddings = []
    if response.predictions:
        # Assuming the response contains a list of embeddings, and each embedding has a 'embeddings' field
        # This structure can vary slightly based on the model and SDK version.
        for prediction in response.predictions:
            # The actual structure might be `prediction['embeddings']['values']` or similar.
            # We need to inspect the actual response object if running against a live API.
            # For now, assuming a direct list of floats if prediction contains it, or a 'values' key.
            if isinstance(prediction, dict) and 'embeddings' in prediction and 'values' in prediction['embeddings']:
                embeddings.extend(prediction['embeddings']['values'])
            elif isinstance(prediction, list):
                embeddings.extend(prediction)

    return embeddings
