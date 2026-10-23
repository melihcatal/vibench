from google.cloud import aiplatform

def invoke_vertex_model(project_id: str, location: str, model_id: str, prompt: str):
    """Invokes a Vertex AI model."""
    client = aiplatform.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
    endpoint = client.endpoint_path(project=project_id, location=location, endpoint=model_id)

    # For models like gemini-pro, the input instance format is typically like this:
    instances = [{"prompt": prompt}]
    parameters = {"temperature": 0.7, "maxOutputTokens": 1024}

    response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)
    # Assuming the response structure for a text model like gemini-pro
    # Adjust based on the specific model's output format
    predictions = response.predictions
    if predictions:
        return predictions[0] # Return the first prediction content
    return None

if __name__ == '__main__':
    # Example usage (replace with your actual project, location, and model)
    project_id = "your-gcp-project-id"
    location = "us-central1"
    model_id = "gemini-pro" # Or an endpoint ID if using a deployed model
    prompt = "Tell me a short story about a brave knight."
    output = invoke_vertex_model(project_id, location, model_id, prompt)
    print(f"Model Output: {output}")
