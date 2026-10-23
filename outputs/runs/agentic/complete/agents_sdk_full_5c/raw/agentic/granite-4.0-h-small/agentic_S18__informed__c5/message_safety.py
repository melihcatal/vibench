# message_safety.py
# LATER-STEP: scan message payload text for unsafe or policy‑violating content (example uses watsonx.ai guardrails)

from ibm_watsonx_ai import ServiceClient
from ibm_watsonx_ai.consts import WatsonxServiceType
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Configure Watsonx guardrails client
class Guardrails:
    def __init__(self, api_key: str, project_id: str):
        # watsonx.ai uses IAM tokens for service
        authenticator = IAMAuthenticator(api_key)
        self.client = ServiceClient(base_url="https://api.us-south.watsonx.ai",
                                    service_type=WatsonxServiceType.GUARDRAILS,
                                    authenticator=authenticator,
                                    project_id=project_id)

    def is_safe(self, text: str) -> bool:
        """Check if the supplied text passes watsonx guardrails safety checks.
        Returns True if safe, False otherwise.
        """
        resp = self.client.chat_with_guarded_moderation(input=text)
        # The response includes a \"moderation\" field with verdicts
        verdict = resp.get("moderation", [{}])[0].get("label")
        # Simple heuristic – if \"safe\" label present, approve
        return verdict == "safe"

# Example usage (requires IBM Cloud API key and project ID)
# guard = Guardrails(os.getenv("WATSONX_API_KEY"), os.getenv("WATSONX_PROJECT_ID"))
# print(guard.is_safe(\"This is a harmless test message.\"))
