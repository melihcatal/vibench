from google.cloud import aiplatform

def select_platform_resource(resource_name: str, project_id: str, location: str):
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    client = aiplatform.gapic.ModelServiceClient(client_options=client_options)
    model_name = client.model_path(project_id, location, resource_name)
    model = client.get_model(name=model_name)
    return {"resource_id": model.name, "display_name": model.display_name}