import google.cloud.aiplatform as aiplatform

def invoke_vertex_ai_model(
    project_id: str,
    location: str,
    model_name: str,
    prompt: str,
) -> str:
    """Invokes a Google Cloud Vertex AI managed model.

    Args:
        project_id: Your Google Cloud project ID.
        location: The region of the Vertex AI model (e.g., "us-central1").
        model_name: The name of the model to invoke (e.g., "gemini-pro").
        prompt: The input prompt for the model.

    Returns:
        The model's generated text response.
    """
    aiplatform.init(project=project_id, location=location)

    # For text models, use TextGenerationModel
    # For other models, you might use different classes (e.g., ImageGenerationModel)
    model = aiplatform.TextGenerationModel.from_pretrained(model_name)
    response = model.predict(prompt=prompt)
    return response.text
