
from google.cloud import aiplatform

def collect_platform_metadata(project_id: str, location: str, model_id: str, prompt: str):
    aiplatform.init(project=project_id, location=location)
    
    # Initialize the model
    model = aiplatform.get_model(model_id)

    # Make a prediction
    instances = [
        {"prompt": prompt},
    ]
    response = model.predict(instances=instances)

    # Extract model output
    model_output = response.predictions[0]

    # Collect platform metadata (simulated with model_id for demonstration)
    platform_metadata = {
        "model_id": model_id,
        "resource_id": model.resource_name,  # Vertex AI resource name as a form of resource ID
        # In a real scenario, more metadata like usage could be extracted from response.metadata or headers
        # For this example, we'll keep it simple with readily available information.
    }

    return {
        "model_output": model_output,
        "platform_metadata": platform_metadata,
    }

