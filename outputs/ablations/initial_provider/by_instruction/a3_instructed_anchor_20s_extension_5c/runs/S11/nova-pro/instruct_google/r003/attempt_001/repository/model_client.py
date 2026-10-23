from google.cloud import aiplatform

def get_client(project_id, location):
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    return client
