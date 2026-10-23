from google.cloud import aiplatform

class EmbeddingsClient:
    def __init__(self, project_id: str, location: str, model_name: str = "text-embedding-004"):
        self.project_id = project_id
        self.location = location
        self.model_name = model_name
        aiplatform.init(project=self.project_id, location=self.location)
        self.client = aiplatform.gapic.PredictionServiceClient()

    def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        instances = [{"content": text} for text in texts]
        endpoint = (
            f"projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.model_name}"
        )
        response = self.client.predict(endpoint=endpoint, instances=instances)
        embeddings = []
        for prediction in response.predictions:
            embeddings.append(list(prediction["embeddings"]["values"]))
        return embeddings
