import os
from google.cloud import aiplatform

def stream_platform_generation(project_id, location, endpoint_id, instances):
    aiplatform.init(project=project_id, location=location)
    endpoint = aiplatform.Endpoint(endpoint_id)
    predictions = endpoint.predict(instances=instances, streaming=True)
    for prediction in predictions:
        yield prediction