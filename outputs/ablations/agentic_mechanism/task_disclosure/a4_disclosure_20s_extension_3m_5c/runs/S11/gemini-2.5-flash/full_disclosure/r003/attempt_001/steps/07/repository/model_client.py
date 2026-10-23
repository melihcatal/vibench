from google.cloud import aiplatform

class ModelClient:
    def __init__(self, project_id: str, location: str):
        self.project_id = project_id
        self.location = location
        aiplatform.init(project=self.project_id, location=self.location)
        self.client = aiplatform.gapic.PredictionServiceClient()

    def get_prediction_service_client(self):
        return self.client

    # Add other helper utilities as needed
