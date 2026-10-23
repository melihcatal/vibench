import os
from google.cloud import aiplatform

def get_client(project_id, location):
    aiplatform.init(project=project_id, location=location)
    return aiplatform

if __name__ == "__main__":
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = 'us-central1'
    client = get_client(project_id, location)
    print(client)