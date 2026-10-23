import os
import json
from model_client import ManagedModelClient
from model_models import ModelInvocationResponse


# Azure OpenAI Content Safety – endpoint and key expected in environment
class PlatformOutputSafety:
    """
    Run Azure OpenAI Content Safety (Guardrails) on model output.
    Returns safe content flag and any moderation details.
    """

    ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    API_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not ENDPOINT:
        raise RuntimeError("AZURE_CONTENT_SAFETY_ENDPOINT not set")
    if not API_KEY:
        raise RuntimeError("AZURE_CONTENT_SAFETY_KEY not set")


def check_output(self, response: ModelInvocationResponse) -> dict:
    """Process raw output string(s) and return moderation metadata."""
    # Content Safety API expects a JSON payload with list of content items
    payload = json.dumps(
        {
            "content": [response.choices[0]["message"]["content"]],
            "model": response.model,
        }
    )
    # Call REST API (curl example shown; in production use http.client or requests)
    # For brevity we use openai's built‑in safety client (AzureContentSafety client)
    from azure.ai.contentsafety import AzureContentSafetyClient

    client = AzureContentSafetyClient(endpoint=self.ENDPOINT, credential=self.API_KEY)
    result = client.analyze_content(text=payload)
    return {
        "content_safe": result.results[0].is_safe,
        "moderation_tags": [tag.name for tag in result.results[0].categories],
    }
