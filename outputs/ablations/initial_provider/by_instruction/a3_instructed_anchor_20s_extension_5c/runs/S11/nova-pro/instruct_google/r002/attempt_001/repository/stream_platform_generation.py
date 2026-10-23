import os
from google.cloud import aiplatform

def stream_generation(project_id, location, endpoint_id, instances):
    aiplatform.init(project=project_id, location=location)
    endpoint = aiplatform.Endpoint(endpoint_id)
    predictions = endpoint.predict(instances=instances, streaming=True)
    for prediction in predictions:
        yield prediction

if __name__ == "__main__":
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = 'us-central1'
    endpoint_id = 'your-endpoint-id'
    instances = [{'content': 'Hello, world!'}]
    for prediction in stream_generation(project_id, location, endpoint_id, instances):
        print(prediction)