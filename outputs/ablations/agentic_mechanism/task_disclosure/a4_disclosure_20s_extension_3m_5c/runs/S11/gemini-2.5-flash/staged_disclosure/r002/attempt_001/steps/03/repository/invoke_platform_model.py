import os
from google.cloud import aiplatform

# Initialize Vertex AI client
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or configure authentication
# For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
# Or using `gcloud auth application-default login`
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
location = "us-central1"  # e.g., "us-central1"

aiplatform.init(project=project_id, location=location)

def invoke_model(prompt: str):
    """Invokes a Google Cloud Vertex AI managed model."""
    try:
        # Use a text-bison model for text generation
        model = aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
        
        # The model ID for text-bison is usually 'text-bison@001' or similar
        # Check the Vertex AI documentation for the exact model ID to use
        endpoint = model.endpoint_path(
            project=project_id, location=location, endpoint="text-bison@001" # This is a placeholder, replace with actual endpoint name if needed
        )
        
        # Prepare the instance for the prediction request
        # For text-bison, the input is typically a `text` field
        instances = [{"prompt": prompt}]
        
        # Make the prediction request
        response = model.predict(endpoint=endpoint, instances=instances)
        
        # Process and return the prediction
        predictions = response.predictions
        if predictions:
            # The structure of predictions can vary by model.
            # For text-bison, it often contains a 'content' field.
            return predictions[0].get("content", "No content in prediction")
        else:
            return "No predictions returned."
            
    except Exception as e:
        return f"Error invoking model: {e}"

if __name__ == "__main__":
    test_prompt = "What is the capital of France?"
    print(f"Invoking model with prompt: '{test_prompt}'")
    result = invoke_model(test_prompt)
    print(f"Model response: {result}")

    test_prompt_2 = "Write a short poem about a cat."
    print(f"Invoking model with prompt: '{test_prompt_2}'")
    result_2 = invoke_model(test_prompt_2)
    print(f"Model response: {result_2}")
