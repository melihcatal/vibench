import os
from google.cloud import aiplatform

def select_platform_resource(project_id, location, model_id):
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.Model(model_id)
    return model.resource_name