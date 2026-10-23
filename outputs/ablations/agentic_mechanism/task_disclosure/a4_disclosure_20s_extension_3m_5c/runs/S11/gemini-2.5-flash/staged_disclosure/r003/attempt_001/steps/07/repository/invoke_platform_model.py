import os
from google.cloud import aiplatform

def invoke_model(project_id: str, location: str, publisher: str, model_id: str, instances: list) -> dict:
    """
    Invokes a provider-managed model through a project-, deployment-, or inference-profile-scoped platform client.

    Args:
        project_id: Your Google Cloud project ID.
        location: The region of the model (e.g., "us-central1").
        publisher: The publisher of the model (e.g., "google").
        model_id: The ID of the model to invoke (e.g., "text-bison@001").
        instances: A list of instances to send to the model for prediction.

    Returns:
        The prediction response from the model.
    """
    
    aiplatform.init(project=project_id, location=location)
    
    # Initialize the prediction client
    client = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    )
    
    # Construct the endpoint name
    endpoint = client.model_path(project_id, location, model_id)

    # Prepare the request
    # For text-bison, instances should be a list of dictionaries, where each dict has a "prompt" key
    formatted_instances = [{"prompt": instance} if isinstance(instance, str) else instance for instance in instances]
    
    response = client.predict(endpoint=endpoint, instances=formatted_instances)
    
    return response.predictions

if __name__ == "__main__":
    # Example usage:
    # Set your Google Cloud project ID and model details
    # Make sure you have authenticated to GCP (e.g., gcloud auth application-default login)
    
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    LOCATION = "us-central1"  # e.g., "us-central1"
    PUBLISHER = "google"
    MODEL_ID = "text-bison@001"  # Example: "text-bison@001" for a generative text model

    if PROJECT_ID == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable or replace 'your-gcp-project-id' with your actual project ID.")
    else:
        # Example instances for a text model
        input_instances = [
            "What is the capital of France?",
            "Write a short poem about nature."
        ]

        print(f"Invoking model {MODEL_ID} in project {PROJECT_ID}...")
        try:
            predictions = invoke_model(PROJECT_ID, LOCATION, PUBLISHER, MODEL_ID, input_instances)
            for i, prediction in enumerate(predictions):
                print(f"Prediction {i+1}: {prediction}")
        except Exception as e:
            print(f"An error occurred: {e}")
