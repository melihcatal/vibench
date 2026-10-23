from google.cloud import aiplatform
from typing import List, Dict, Any


class MeetingSummarizer:
    """Summarizes live meeting transcript chunks."""

    def __init__(self, model_id: str = "text-bison@002"):
        aiplatform.init(project="your-project-id", location="us-central1")
        self.model = aiplatform.Model(model_name=model_id)
        self.endpoint = self.model.deploy(machine_type="n1-standard-4")

    async def summarize_chunks(self, chunks: List[str]) -> str:
        """Summarizes a list of transcript chunks into a concise meeting summary."""
        combined_text = " ".join(chunks)
        prompt = f"Summarize the following meeting transcript:\n\n{combined_text}\n\nSummary:"

        response = self.endpoint.predict(instances=[{"prompt": prompt}])
        return response.predictions[0]
