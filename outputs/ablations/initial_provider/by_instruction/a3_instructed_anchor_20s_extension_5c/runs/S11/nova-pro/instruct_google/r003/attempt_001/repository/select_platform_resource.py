from google.cloud import aiplatform

def select_resource(project_id, location):
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    client = aiplatform.gapic.EndpointServiceClient(client_options=client_options)
    parent = f"projects/{project_id}/locations/{location}"
    response = client.list_endpoints(parent=parent)
    return response
