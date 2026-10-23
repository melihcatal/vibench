import os
from google.cloud import aiplatform

def collect_metadata(project_id, location, endpoint_id, instances):
    aiplatform.init(project=project_id, location=location)
    endpoint = aiplatform.Endpoint(endpoint_id)
    predictions = endpoint.predict(instances=instances)
    metadata = predictions._prediction_metadata
    return metadata

if __name__ == "__main__":
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = 'us-central1'
    endpoint_id = 'your-endpoint-id'
    instances = [{'content': 'Hello, world!'}]
    result = collect_metadata(project_id, location, endpoint_id, instances)
    print(result)