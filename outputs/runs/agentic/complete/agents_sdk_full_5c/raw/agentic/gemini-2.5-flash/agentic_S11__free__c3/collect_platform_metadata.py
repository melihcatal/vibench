from google.cloud import aiplatform
import json

def collect_vertex_metadata(project_id: str, location: str, model_id: str, prompt: str):
    """Returns model output together with provider platform metadata."""
    client = aiplatform.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
    endpoint = client.endpoint_path(project=project_id, location=location, endpoint=model_id)

    instances = [{"prompt": prompt}]
    parameters = {"temperature": 0.1, "maxOutputTokens": 512}

    # Provider-identifying signal: google.cloud.aiplatform.PredictionServiceClient
    response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)

    model_output = None
    if response.predictions:
        # Assuming text generation, content is usually in the first prediction
        model_output = response.predictions[0]

    # Extracting relevant metadata. The exact structure can vary by model.
    # For Gemini models, usage metadata might be in the candidate or in the overall response.
    # For the purpose of this example, we'll create a dictionary for metadata.
    platform_metadata = {
        "model_id": model_id,
        "project_id": project_id,
        "location": location,
        "deployed_model_id": response.deployed_model_id, # This is often present
        "model_parameters": parameters, # Parameters sent to the model
        # More metadata could be extracted from response.metadata if available
    }

    return {"output": model_output, "metadata": platform_metadata}

if __name__ == '__main__':
    # Example usage (replace with your actual project, location, and model)
    project_id = "your-gcp-project-id"
    location = "us-central1"
    model_id = "gemini-pro" 
    prompt = "Summarize the plot of Romeo and Juliet in one sentence."

    result = collect_vertex_metadata(project_id, location, model_id, prompt)
    print(f"Model Output: {result['output']}")
    print(f"Platform Metadata: {json.dumps(result['metadata'], indent=2)}")
