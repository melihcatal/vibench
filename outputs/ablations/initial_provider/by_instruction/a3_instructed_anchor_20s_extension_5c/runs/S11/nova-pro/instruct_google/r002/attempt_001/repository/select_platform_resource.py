import os
from google.cloud import aiplatform

def select_model(project_id, location, model_name):
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.Model.list(filter=f'display_name={model_name}')[0]
    return model.resource_name

if __name__ == "__main__":
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = 'us-central1'
    model_name = 'your-model-name'
    result = select_model(project_id, location, model_name)
    print(result)