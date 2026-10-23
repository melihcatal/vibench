import os
from google.cloud import aiplatform

def select_model_resource(project_id: str, location: str, model_id: str):
    aiplatform.init(project=project_id, location=location)
    
    # In a real scenario, you would list/get models or deployments
    # and select one based on criteria. For this example, we'll 
    # simulate selection by just returning a model resource name.
    
    # Example: projects/{project}/locations/{location}/models/{model_id}
    # Or, if it's a deployed model: 
    # projects/{project}/locations/{location}/endpoints/{endpoint_id}/deployedModels/{deployed_model_id}
    
    model_resource_name = f"projects/{project_id}/locations/{location}/models/{model_id}"
    print(f"Selected model resource: {model_resource_name}")
    return model_resource_name

