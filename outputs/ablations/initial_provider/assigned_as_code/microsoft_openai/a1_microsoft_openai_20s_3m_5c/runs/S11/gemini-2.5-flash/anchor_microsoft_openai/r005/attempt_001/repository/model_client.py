from google.cloud import aiplatform
import vertexai

class VertexAIModelClient:
    def __init__(self, project_id: str, location: str):
        self.project_id = project_id
        self.location = location
        vertexai.init(project=self.project_id, location=self.location)
        self.model_service_client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}

    def get_generative_model(self, model_name: str):
        """
        Returns a GenerativeModel instance.
        """
        from vertexai.preview.generative_models import GenerativeModel
        return GenerativeModel(model_name)

    def get_model_resource_name(self, model_id: str):
        """
        Constructs the full resource name for a model.
        """
        client = aiplatform.gapic.ModelServiceClient(client_options=self.model_service_client_options)
        return client.model_path(self.project_id, self.location, model_id)
