from google.cloud import aiplatform
from typing import List, Dict, Any


class MeetingSummarizer:
    """Summarizes live meeting transcript chunks using Google Cloud Vertex AI."""

    def __init__(self, model_id: str = "text-bison@002"):
        aiplatform.init(project="your-project-id", location="us-central1")
        self.model = aiplatform.Model(model_name=model_id)

    async def summarize_chunks(self, chunks: List[str]) -> str:
        """Summarizes a list of transcript chunks."""
        prompt = (
            "Summarize the following meeting transcript chunks into a concise summary:\n\n"
            f"{' '.join(chunks)}"
        )
        response = self.model.predict(instances=[{"prompt": prompt}])
        return response.predictions[0]
