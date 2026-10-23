import os
from ibm_watsonx_ai import WatsonxAiClient
from ibm_watsonx_ai.consts import EndpointType, ServiceName
from safety_models import Prompt, Response


class AppealTranslate:
    def __init__(self):
        self.client = WatsonxAiClient(
            service=ServiceName.TEXT_CHAT,
            api_key=os.getenv("WATSONX_API_KEY"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
            endpoint=EndpointType.REGION,
        )

    def translate_appeal(self, appeal_text: str, target_lang: str = "en") -> str:
        # Simple placeholder: call watsonx chat to translate the appeal.
        # In practice you'd use a translation model or service.
        prompt = Prompt.request(appeal_text)
        raw = self.client.chat_completion(prompt)
        # Expect response with field "translation"
        return Response.normalize(raw)["translation"]
