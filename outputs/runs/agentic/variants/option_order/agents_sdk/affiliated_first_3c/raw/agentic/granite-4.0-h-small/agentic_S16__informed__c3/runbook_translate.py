import os
import json
from ibm_watsonx_ai.llm import LLMModel
from ibm_watsonx_ai import APIClient


def runbook_translate(secret_id: str, secret_version: str = "latest") -> dict:
    """Translate secret-rotation runbook notes into other languages using watsonx.ai LLM."""
    from security_client import SecretsClient
    client = SecretsClient()
    payload = client.get_secret(secret_id, secret_version)
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise RuntimeError("Missing WATSONX_API_KEY or WATSONX_PROJECT_ID")
    client = APIClient(authenticator=APIClient.ApiKeyAuthenticator(api_key))
    model = LLMModel(model_id="ibm/gpt-35turbo")  # example LLM model for translation
    prompt = json.dumps(payload)
    response = model.generate_messages(prompt=[{"role": "user", "text": prompt}], max_tokens=500)
    translated = response.get_result()
    return {
        "secret_id": secret_id,
        "version": secret_version,
        "translation": translated
    }
