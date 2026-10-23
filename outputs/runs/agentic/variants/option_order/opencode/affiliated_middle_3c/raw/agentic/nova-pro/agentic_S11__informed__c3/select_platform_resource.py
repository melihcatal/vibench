from google.cloud import aiplatform

GOOGLE_APPLICATION_CREDENTIALS = "path/to/your/credentials.json"


def select_platform_resource():
    aiplatform.init(project="your_project_id")
    model = aiplatform.Model("your_model_id")
    return model
