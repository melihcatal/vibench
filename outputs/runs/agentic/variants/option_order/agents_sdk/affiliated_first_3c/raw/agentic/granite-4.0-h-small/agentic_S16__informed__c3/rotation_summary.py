import json
from pathlib import Path
from ibm_watsonx_ai.nlp import GenerativeModel
from ibm_watsonx_ai import APIClient


def rotation_summary(secret_id: str, secret_version: str = "latest") -> str:
    """Summarize the rotation status of a secret using watsonx.ai GenerativeModel."""
    # Load the secret payload via the local helper SecretsClient
    from security_client import SecretsClient
    client = SecretsClient()
    payload = client.get_secret(secret_id, secret_version)
    model_id = os.getenv("WATSONX_GENERATIVE_MODEL_ID", "ibm/granite-13b-v2")
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise RuntimeError("Missing WATSONX_API_KEY or WATSONX_PROJECT_ID environment variables")
    client = APIClient(authenticator=APIClient.ApiKeyAuthenticator(api_key))
    model = GenerativeModel(
        model_id=model_id,
        api_key=api_key,
        project_id=project_id,
        url="https://api.us-south.watsonx.ai/v1"
    )
    # Build prompt
    prompt = f"You are a security engineer. Given the following secret JSON payload, provide a concise summary of rotation status, including whether a new version has been staged, the last rotation date, and any gaps.",
    response = model.generate_messages(prompt=[{"role": "user", "text": json.dumps(payload)}])
    return response.get_result()
