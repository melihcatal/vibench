import google.cloud.aiplatform as aiplatform

def select_platform_resource(model_name: str, project_id: str, location: str):
    """
    Resolves a provider-specific model resource before invocation using Google Cloud Vertex AI.
    """
    # Initialize the AI Platform client
    aiplatform.init(project=project_id, location=location)

    # Get a model resource. In a real scenario, you might get a deployed model or a base model.
    # For demonstration, we'll assume we are looking for a base model.
    # The model_name could be something like "text-bison@001" or a custom model ID.
    model_resource_name = f"projects/{project_id}/locations/{location}/models/{model_name}"
    
    # In a real application, you would use the model_resource_name to interact with the model.
    # For example: model = aiplatform.Model(model_resource_name)
    # However, directly instantiating aiplatform.Model might require authentication
    # and a valid model existing in the specified project/location.
    # Here, we'll just return the resolved resource name to fulfill the task of "resolves a provider-specific model resource".
    return model_resource_name

