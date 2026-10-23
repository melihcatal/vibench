import os
from google.cloud import aiplatform

def collect_platform_metadata(project_id, location, endpoint_id, instances):
    aiplatform.init(project=project_id, location=location)
    endpoint = aiplatform.Endpoint(endpoint_id)
    predictions = endpoint.predict(instances=instances)
    metadata = predictions.metadata
    return metadata