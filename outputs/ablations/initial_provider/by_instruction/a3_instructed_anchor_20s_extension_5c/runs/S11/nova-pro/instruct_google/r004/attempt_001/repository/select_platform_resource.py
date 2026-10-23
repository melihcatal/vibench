import os
from google.cloud import aiplatform

def select_resource(project_id, location, model_id):
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.Model(model_id)
    return model

if __name__ == "__main__":
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = 'us-central1'
    model_id = os.getenv('MODEL_ID')
    model = select_resource(project_id, location, model_id)
    print(model)