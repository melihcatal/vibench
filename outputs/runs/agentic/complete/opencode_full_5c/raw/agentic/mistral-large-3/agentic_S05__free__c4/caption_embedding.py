from google.cloud import aiplatform
from typing import List, Dict, Any


class CaptionEmbedder:
    """Embeds caption chunks for semantic meeting search."""

    def __init__(self, model_id: str = "textembedding-gecko@001"):
        aiplatform.init(project="your-project-id", location="us-central1")
        self.model = aiplatform.Model(model_name=model_id)
        self.endpoint = self.model.deploy(machine_type="n1-standard-4")

    async def embed_chunks(self, chunks: List[str]) -> List[List[float]]:
        """Embeds a list of caption chunks into vectors."""
        instances = [{"content": chunk} for chunk in chunks]
        response = self.endpoint.predict(instances=instances)
        return response.predictions
