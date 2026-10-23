import openai
from typing import Any, Dict, List
from security_models import SecretModel, RotatedSecret

def runbook_translate(secret_id: str, openai_api_key: str, model: str = 'gpt-4o') -> Dict[str, Any]:
    """Translates secret rotation runbook notes from one language to another using OpenAI's API.

    Steps performed:
        1. Retrieve the secret (expected to contain a 'runbook' field with the original runbook text).
        2. Call OpenAI Chat Completion with a system prompt that explains the translation task.
        3. Return the translated text as part of a RotatedSecret model.
    """
    client = openai.OpenAI(api_key=openai_api_key)
    # Fetch secret payload
    raw = client.get_secret_value(SecretId=secret_id)
    payload = raw.get('SecretString')
    if not payload:
        raise ValueError('Secret does not contain runbook notes')
    runbook_text = json.loads(payload).get('runbook')
    if not runbook_text:
        raise ValueError('No runbook found in secret payload')
    # Translate using chat completion (simple prompt)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': 'You are an expert in cloud security and will translate the given runbook from its current language to English while preserving technical details.'},
            {'role': 'user', 'content': runbook_text}
        ]
    )
    translated = response.choices[0].message.content
    rotated = RotatedSecret(secret_id)
    rotated.set_rotation_timestamp('2025-08-24T12:00:00Z')
    rotated.payload['translated_runbook'] = translated
    return rotated.payload
