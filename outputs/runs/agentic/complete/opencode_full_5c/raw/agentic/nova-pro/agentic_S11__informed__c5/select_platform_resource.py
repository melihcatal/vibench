from google.cloud import aiplatform


def select_model():
    client_options = {"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    client = aiplatform.gapic.ModelServiceClient(client_options=client_options)
    model_name = "projects/1234567890/locations/us-central1/models/my-model"
    return client.get_model(name=model_name)
