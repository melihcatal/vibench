from google.cloud import aiplatform

def invoke_platform_model(project_id: str, location: str, model_name: str, prompt: str):
    """Invokes a Google Vertex AI managed model.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region where the model is deployed.
        model_name: The name or ID of the model to invoke (e.g., "text-bison@001").
        prompt: The input prompt for the model.

    Returns:
        The model's generated text response.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.TextGenerationModel.from_pretrained(model_name)
    response = model.predict(prompt)
    return response.text
