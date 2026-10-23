from google.cloud import aiplatform

def init_aiplatform(project_id, location):
    aiplatform.init(project=project_id, location=location)

def get_model(model_id):
    return aiplatform.Model(model_id)