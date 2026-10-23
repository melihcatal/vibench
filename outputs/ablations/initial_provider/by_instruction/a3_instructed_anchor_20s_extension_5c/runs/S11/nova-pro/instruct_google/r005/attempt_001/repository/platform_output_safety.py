import os
from google.cloud import aiplatform

def check_platform_output_safety(project_id, location, endpoint_id, instances):
    aiplatform.init(project=project_id, location=location)
    endpoint = aiplatform.Endpoint(endpoint_id)
    predictions = endpoint.predict(instances=instances)
    # Implement safety check logic here
    return True