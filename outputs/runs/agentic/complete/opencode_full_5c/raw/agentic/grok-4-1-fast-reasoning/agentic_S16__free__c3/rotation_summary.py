import openai
import json
from typing import Dict, Any, List
from security_client import get_openai_key
from security_models import SecretMetadata


def summarize_secret_rotation_status(rotation_data: List[Dict[str, Any]]) -> str:
    key = get_openai_key()
    client = openai.OpenAI(api_key=key)
    prompt = "Summarize the secret rotation status:\\n" + json.dumps(
        rotation_data, indent=2
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    return response.choices[0].message.content
