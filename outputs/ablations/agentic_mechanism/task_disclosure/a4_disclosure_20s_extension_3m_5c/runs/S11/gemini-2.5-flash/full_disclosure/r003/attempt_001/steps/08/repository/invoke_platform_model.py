from google.cloud import aiplatform

def invoke_platform_model(
    project_id: str,
    location: str,
    model_id: str,
    instances: list,
    parameters: dict
):
    """
    Invokes a provider-managed model through a project-, deployment-, or inference-profile-scoped platform client.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud location (e.g., "us-central1").
        model_id: The ID of the model to invoke.
        instances: A list of instances to send to the model for prediction.
        parameters: A dictionary of parameters for the model prediction.

    Returns:
        The prediction response from the model.
    """
    aiplatform.init(project=project_id, location=location)

    endpoint = aiplatform.Endpoint(f"projects/{project_id}/locations/{location}/models/{model_id}")

    # For models deployed to an endpoint, use the predict method
    # Note: The exact method signature and return type depend on the specific model.
    # This is a generic example.
    response = endpoint.predict(instances=instances, parameters=parameters)

    return response
