import os
from ibm_watsonx_ai import WatsonxAiClient
from ibm_watsonx_ai.consts import EndpointType, ServiceName
from safety_models import Prompt, Response


class ModerationReasonEmbedding:
    def __init__(self):
        self.client = WatsonxAiClient(
            service=ServiceName.EMBEDDING,
            api_key=os.getenv("WATSONX_API_KEY"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
            endpoint=EndpointType.REGION,
        )

    def embed(self, rationale: str) -> str:
        embeddings = self.client.embed(model_id="text-embedding")
        # The SDK returns an object; we just call .embed for simplicity
        return embeddings["embeddings"][0]["vector"]
