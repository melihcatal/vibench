from google.cloud import aiplatform

def invoke_model(project_id: str, location: str, model_name: str, prompt: str):
    """
    Invokes a provider-managed model through a project-, deployment-, or inference-profile-scoped platform client.
    Using Google Cloud Vertex AI as the concrete provider.
    """
    aiplatform.init(project=project_id, location=location)

    # Load the model
    model = aiplatform.PreviewModel.from_pretrained(model_name)

    # Make a prediction
    response = model.predict(prompt)
    return response.predictions[0]
