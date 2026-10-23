from google.cloud import aiplatform

def invoke_platform_model(project_id: str, location: str, model_id: str, prompt: str):
    """Invokes a Google Cloud Vertex AI managed model."""
    aiplatform.init(project=project_id, location=location)
    
    # Use the TextGenerationModel for ease of use with text prompts
    # For more complex scenarios, PredictionServiceClient might be used directly
    model = aiplatform.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
    
    # Example using a common generative text model
    instance = {"prompt": prompt}
    parameters = {"temperature": 0.7, "max_output_tokens": 200}
    
    # The endpoint needs to be specified correctly for the model
    # For common generative models, it's often projects/PROJECT_ID/locations/LOCATION/publishers/google/models/MODEL_ID
    # For custom deployed models, it would be projects/PROJECT_ID/locations/LOCATION/endpoints/ENDPOINT_ID
    # This example assumes a publisher model like "gemini-pro"
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"
    
    instances_json = [instance]
    parameters_json = parameters
    
    response = model.predict(endpoint=endpoint, instances=instances_json, parameters=parameters_json)
    
    # The actual structure of the response depends on the model.
    # For Generative AI models, it typically contains 'predictions' which is a list.
    if response.predictions:
        # Assuming the first prediction contains the generated text
        # This might need adjustment based on the exact model output structure
        return response.predictions[0]
    return None

if __name__ == '__main__':
    # Placeholder values for demonstration
    # Replace with your actual project_id, location, and a valid model_id (e.g., 'gemini-pro')
    # For example, model_id='gemini-pro'
    # See https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models for available models
    result = invoke_platform_model(
        project_id="your-gcp-project-id", 
        location="us-central1", 
        model_id="gemini-pro", 
        prompt="Tell me a short story about a brave knight."
    )
    if result:
        print("Generated Text:", result)
    else:
        print("No generation received.")
