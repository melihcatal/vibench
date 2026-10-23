from google.cloud import aiplatform

def select_platform_resource(project_id: str, location: str, model_display_name: str) -> str:
    """
    Resolves a Google Cloud Vertex AI model resource ID by its display name.
    """
    aiplatform.init(project=project_id, location=location)
    
    client = aiplatform.ModelServiceClient(client_options={'api_endpoint': f'{location}-aiplatform.googleapis.com'})
    
    parent = f"projects/{project_id}/locations/{location}"
    list_models_request = aiplatform.ListModelsRequest(parent=parent)
    page_result = client.list_models(request=list_models_request)
    
    for model in page_result:
        if model.display_name == model_display_name:
            return model.name.split('/')[-1] # Return the model ID
            
    return ""
