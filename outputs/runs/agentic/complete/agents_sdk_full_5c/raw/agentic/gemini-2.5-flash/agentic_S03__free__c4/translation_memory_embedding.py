from google.cloud import aiplatform

def embed_text_for_translation_memory(text: str) -> list[float]:
    """
    Generates embeddings for translated segments for translation-memory search
    using Google Cloud Vertex AI Text Embeddings API.
    """
    # Vertex AI PredictionServiceClient for text-bison embeddings
    # The endpoint depends on the region.
    project_id = "your-gcp-project-id"  # Replace with your GCP project ID
    location = "us-central1" # Or your desired region
    endpoint_id = "text-embedding-gecko" # Or "text-bison" if using a different model

    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    endpoint = client.endpoint_path(
        project=project_id, location=location, endpoint=endpoint_id
    )

    # For text-embedding-gecko, the input instance format is typically like this:
    instances = [{"content": text}]
    parameters = aiplatform.gapic.PredictRequest.dict_to_protobuf({
        "temperature": 0.0,
        "maxOutputTokens": 128, # Not directly relevant for embeddings but often part of parameters for text models
    }) # For embedding, parameters are usually minimal or not needed

    response = client.predict(
        endpoint=endpoint,
        instances=instances,
        parameters=parameters,
    )

    # Assuming the response structure for embeddings
    if response.predictions:
        # The exact structure can vary. For embeddings, it's usually a list of floats.
        # This is an example, adjust based on actual model output.
        # For 'text-embedding-gecko', the embedding is directly in the prediction.
        embedding = response.predictions[0]["embeddings"]["values"]
        return embedding
    return []
