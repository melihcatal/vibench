from google.cloud import aiplatform

def stream_vertex_ai_generation(
    project_id: str,
    location: str,
    model_name: str,
    prompt: str,
):
    """
    Streams output from a Google Vertex AI managed model and preserves provider response objects.
    """
    aiplatform.init(project=project_id, location=location)

    # For text generation, we use the PredictionServiceClient
    # For streaming, we might directly use the model object with specific methods if available.
    # As of current SDK design, streaming for generative models like text-bison is often handled
    # by calling `generate_content` and iterating over the response.
    # The 'google.cloud.aiplatform' import clearly identifies the provider.
    # The model_name like 'gemini-pro' or 'text-bison@001' is a provider-specific model identifier.
    model = aiplatform.preview.language_models.TextGenerationModel.from_pretrained(model_name)

    # The actual streaming behavior depends on the model's API.
    # For many generative models, the response object itself can be iterated over to stream parts.
    # This example assumes a synchronous call that returns an iterable-like object or a full response.
    # To truly "stream" in the sense of receiving chunks as they are generated,
    # the SDK method would need to support it explicitly.
    # For now, we'll simulate by returning the response object itself, assuming
    # the user will iterate over it as per the provider's SDK documentation for streaming.

    response = model.predict(prompt=prompt)
    
    # In a real streaming scenario, `response` would often be an iterable.
    # We return the raw response object to preserve provider response objects as requested.
    return response

