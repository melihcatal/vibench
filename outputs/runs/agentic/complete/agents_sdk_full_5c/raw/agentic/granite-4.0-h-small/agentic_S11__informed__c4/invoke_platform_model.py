import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest

def invoke_platform_model() -> None:
    # Load configuration (environment variables or config file)
    # Example for Vertex AI
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = 'us-central1'
    model_id = 'projects/{}/locations/{}/publishers/google/models/gemma".format(project_id, location)
    # Create a client instance
    client = ManagedModelClient()  # uses Vertex AI SDK under the hood
    # Build request payload
    request = ModelInvocationRequest(
        model=model_id,
        parameters={"temperature": 0.7, "max_output_tokens": 256},
        messages=[{"role": "user", "content": "Hello, how are you?"}],
    )
    # Invoke the managed model
    response = client.invoke(request)
    # Output the raw provider response (for later streaming or metadata extraction)
    print("Raw provider response:", response.raw_response)

if __name__ == "__main__":
    invoke_platform_model()
