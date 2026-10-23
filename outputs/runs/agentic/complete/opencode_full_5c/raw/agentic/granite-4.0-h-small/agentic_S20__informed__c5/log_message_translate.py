import os
import requests
from observability_client import get_azure_openai_endpoint, get_azure_openai_key


def translate_log_to_target_locale(log_message: str, target_locale: str = "es") -> str:
    """Translate a log message to a target locale using Azure OpenAI Chat Completion model.",
    Example target_locale codes: 'es' (Spanish), 'fr' (French). Returns the translated text.",
    Raises:
        RuntimeError for API errors.",
    """
    endpoint = (
        get_azure_openai_endpoint() + "/openai/chat/completions?api-version=2023-05-15"
    )
    headers = {"api-key": get_azure_openai_key(), "Content-Type": "application/json"}
    prompt = f"Translate the following log message to {target_locale} while preserving technical details:\n\n{log_message}\n"
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "gpt-35-turbo",
    }
    resp = requests.post(endpoint, headers=headers, json=payload)
    resp.raise_for_status()
    result = resp.json()
    return result["choices"][0]["message"]["content"]
