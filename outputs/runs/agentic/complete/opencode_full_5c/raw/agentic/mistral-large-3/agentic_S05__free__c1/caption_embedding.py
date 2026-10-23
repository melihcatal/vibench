from google.cloud import aiplatform
from typing import List, Dict, Any
import numpy as np


class CaptionEmbedder:
    """Embeds caption chunks for semantic meeting search using Google Cloud Vertex AI."""

    def __init__(self, model_id: str = "textembedding-gecko@001"):
        aiplatform.init(project="your-project-id", location="us-central1")
        self.model = aiplatform.Model(model_name=model_id)

    async def embed_chunks(self, chunks: List[str]) -> List[List[float]]:
        """Embeds a list of caption chunks."""
        instances = [{"content": chunk} for chunk in chunks]
        response = self.model.predict(instances=instances)
        return [
            np.array(prediction["embeddings"]["values"]).tolist()
            for prediction in response.predictions
        ]
