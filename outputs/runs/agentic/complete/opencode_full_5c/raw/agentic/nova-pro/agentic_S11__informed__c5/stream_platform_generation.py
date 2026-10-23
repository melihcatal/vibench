from google.cloud import aiplatform


def stream_generation():
    client_options = {"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    model_name = "projects/1234567890/locations/us-central1/models/my-model"
    instances = [{"content": "Hello, world!"}]
    response = client.predict(name=model_name, instances=instances)
    for prediction in response.predictions:
        yield prediction
