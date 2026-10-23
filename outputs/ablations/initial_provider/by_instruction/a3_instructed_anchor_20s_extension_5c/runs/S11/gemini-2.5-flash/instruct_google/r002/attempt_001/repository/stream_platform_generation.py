from google.cloud import aiplatform

def stream_platform_generation(project_id: str, location: str, model_id: str, prompt: str):
    """Streams output from a Google Cloud Vertex AI model."""
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.Model.create(model_id=model_id)
    # Assuming the model supports streaming, this is a placeholder.
    # Actual streaming would involve iterating over a generator.
    response_iterator = model.predict_streaming(instances=[{"prompt": prompt}])
    for response in response_iterator:
        yield response
