from google.cloud import aiplatform

def invoke_model(project_id, location, endpoint_id, instances):
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    endpoint = f"projects/{project_id}/locations/{location}/endpoints/{endpoint_id}"
    response = client.predict(endpoint=endpoint, instances=instances)
    return response
