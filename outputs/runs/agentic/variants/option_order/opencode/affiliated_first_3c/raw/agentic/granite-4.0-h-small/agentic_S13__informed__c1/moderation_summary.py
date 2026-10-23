import os
from ibm_watsonx_ai import WatsonxAiClient
from ibm_watsonx_ai.consts import EndpointType, ServiceName
from safety_models import Prompt, Response


class ModerationSummary:
    def __init__(self):
        self.client = WatsonxAiClient(
            service=ServiceName.TEXT_CHAT,
            api_key=os.getenv("WATSONX_API_KEY"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
            endpoint=EndpointType.REGION,
        )

    def summarize(self, moderation_results: list[dict]) -> str:
        # Convert results to human-readable bullet points
        lines = [f"- {r['category']}: {r['score']:.2f}" for r in moderation_results]
        return "Moderation summary:\n" + "\n".join(lines)
