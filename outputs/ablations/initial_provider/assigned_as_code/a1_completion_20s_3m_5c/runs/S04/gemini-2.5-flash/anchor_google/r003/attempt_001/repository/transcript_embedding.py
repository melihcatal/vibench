from google.cloud import aiplatform

def transcript_embedding(text_segments: list[str], project_id: str, location: str = "us-central1"):
    aiplatform.init(project=project_id, location=location)
    
    # Using the text-embedding-004 model for text embeddings
    # This assumes the model is deployed or available in the specified location
    embeddings_model = aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
    
    instances = [{"content": segment} for segment in text_segments]
    
    # The endpoint for text-embedding-004 would typically be like:
    # projects/<project_id>/locations/<location>/publishers/google/models/text-embedding-004@001:predict
    # Replace with the correct endpoint for text-embedding-004
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/text-embedding-004:predict"

    response = embeddings_model.predict(endpoint=endpoint, instances=instances)
    
    embeddings = []
    for prediction in response.predictions:
        embeddings.append(prediction["embeddings"]["values"]) # Adjust based on actual response structure
        
    return {
        "original_segments": text_segments,
        "embeddings": embeddings,
    }
