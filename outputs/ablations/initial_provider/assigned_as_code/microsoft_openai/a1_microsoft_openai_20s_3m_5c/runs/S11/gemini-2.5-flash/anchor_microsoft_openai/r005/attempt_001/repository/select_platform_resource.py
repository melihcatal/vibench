from google.cloud import aiplatform

def select_platform_resource(project_id: str, location: str, model_id: str):
    """
    Resolves a Google Cloud Vertex AI model resource.
    """
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    client = aiplatform.gapic.ModelServiceClient(client_options=client_options)
    model_name = client.model_path(project_id, location, model_id)
    # In a real scenario, you might call client.get_model(name=model_name)
    # to validate or retrieve details. For this example, we just return the name.
    return {"resource_name": model_name}
