from google.cloud import secretmanager

from vertexai.language_models import TextGenerationModel


def runbook_translate(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{config['project_id']}/secrets/{payload['secret_id']}"
    secret = client.get_secret(request={"name": name})
    model = TextGenerationModel.from_pretrained("gemini-1.5-flash-002")
    source_text = payload.get("text") or (secret.annotations or {}).get("runbook", "")
    response = model.predict(f"Translate this secret rotation runbook to {payload.get('target_language', 'English')}: {source_text}")
    return {"translation": response.text}
