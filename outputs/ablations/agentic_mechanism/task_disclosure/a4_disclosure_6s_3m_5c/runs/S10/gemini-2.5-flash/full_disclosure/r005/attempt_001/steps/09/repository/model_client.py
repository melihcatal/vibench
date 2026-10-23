from google.cloud import aiplatform

class ModelClient:
    def __init__(self, project_id: str, location: str, model_name: str = "text-bison@001"):
        self.project_id = project_id
        self.location = location
        self.model_name = model_name
        aiplatform.init(project=self.project_id, location=self.location)
        self.model = aiplatform.TextGenerationModel.from_pretrained(self.model_name)

    def generate_text(self, prompt: str, **kwargs) -> str:
        response = self.model.predict(prompt, **kwargs)
        return response.text