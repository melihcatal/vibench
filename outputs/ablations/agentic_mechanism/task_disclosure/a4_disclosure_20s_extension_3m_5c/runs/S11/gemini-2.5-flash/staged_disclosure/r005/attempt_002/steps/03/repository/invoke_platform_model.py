
import os
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

def invoke_model():
    # It is recommended to set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # with the path to your service account key file for authentication.
    # For example:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1") # e.g., us-central1
    # This is an example for a Generative AI model.
    # For other models, the model_id and instances structure might differ.
    model_id = os.getenv("GOOGLE_CLOUD_MODEL_ID", "gemini-pro") # e.g., gemini-pro, text-bison@001

    if project_id == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable or update the script.")
        return
    if model_id == "gemini-pro": # Default example model
        print("Using default model_id 'gemini-pro'. Consider setting GOOGLE_CLOUD_MODEL_ID for other models.")


    aiplatform.init(project=project_id, location=location)
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    prediction_client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    # Example for a text-based generative model
    # The instances format varies significantly between models.
    # Consult the specific model's documentation for the correct input format.
    instances = [
        {"prompt": "What is the capital of France?"},
    ]
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 100,
    }

    # Convert instances and parameters to protobuf Value objects
    # This step is crucial for models that expect protobuf.
    # For models that directly accept dictionaries, this conversion might not be needed.
    # Always refer to the model's documentation.
    instances_pb = [json_format.ParseDict(instance, Value()) for instance in instances]
    parameters_pb = json_format.ParseDict(parameters, Value())

    try:
        endpoint = prediction_client.endpoint_path(
            project=project_id, location=location, endpoint=model_id
        )
        response = prediction_client.predict(
            endpoint=endpoint, instances=instances_pb, parameters=parameters_pb
        )

        print("Prediction response:")
        for prediction in response.predictions:
            print(dict(prediction))

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Ensure GOOGLE_APPLICATION_CREDENTIALS is set and the model exists and is deployed.")

if __name__ == "__main__":
    invoke_model()
