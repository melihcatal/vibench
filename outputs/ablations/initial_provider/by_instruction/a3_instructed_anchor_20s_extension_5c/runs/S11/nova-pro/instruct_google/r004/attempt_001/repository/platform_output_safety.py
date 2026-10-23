import os
from google.cloud import aiplatform

def check_safety(project_id, location, endpoint_id, instances):
    aiplatform.init(project=project_id, location=location)
    endpoint = aiplatform.Endpoint(endpoint_id)
    predictions = endpoint.predict(instances=instances)
    safe = all(prediction.safety_ratings[0].score >= 0.5 for prediction in predictions)
    return safe

if __name__ == "__main__":
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = 'us-central1'
    endpoint_id = os.getenv('ENDPOINT_ID')
    instances = [{"content": "Hello, world!"}]
    safe = check_safety(project_id, location, endpoint_id, instances)
    print(safe)