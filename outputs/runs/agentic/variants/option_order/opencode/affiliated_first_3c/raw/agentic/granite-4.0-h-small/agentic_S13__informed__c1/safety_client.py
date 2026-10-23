import os
from ibm_watsonx_ai import WatsonxAiClient
from ibm_watsonx_ai.consts import EndpointType, ServiceName

# Environment variables are expected: WATSONX_API_KEY, WATSONX_PROJECT_ID


class SafetyClient:
    def __init__(self):
        self.watsonx = WatsonxAiClient(
            service=ServiceName.GUARDRAILS,
            api_key=os.getenv("WATSONX_API_KEY"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
            endpoint=EndpointType.REGION,
        )

    def moderate(self, payload):
        return self.watsonx.guardrails_moderate(payload)

    def moderate_batch(self, payloads):
        return self.watsonx.guardrails_moderate_batch(payloads)

    def redact_unsafe(self, payload):
        return self.watsonx.guardrails_redact_unsafe(payload)
