from google.cloud import aiplatform

def embed_transcript_segments(segments: list[str], project_id: str, location: str = "us-central1") -> list[list[float]]:
    # Initialize Vertex AI
    aiplatform.init(project=project_id, location=location)

    # Use a pre-trained embedding model, e.g., 'textembedding-gecko@001'
    # Ensure this model is available or deployed in your Vertex AI project.
    model = aiplatform.get_model_garden_model("textembedding-gecko@001")

    instances = [{'content': segment} for segment in segments]
    
    response = model.predict(instances=instances)
    
    embeddings = []
    if response.predictions:
        for prediction in response.predictions:
            # Assuming prediction['embeddings'] contains the actual embedding vector
            if 'embeddings' in prediction and 'values' in prediction['embeddings']:
                embeddings.append(prediction['embeddings']['values'])
    return embeddings
