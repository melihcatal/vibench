import requests
from safety_client import get_tisane_headers

TISANE_OBFUSCATE_URL = "https://api.tisane.ai/rest/v1/obfuscate"

def redact_unsafe(text: str, language: str = "en") -> str:
    headers = get_tisane_headers()
    data = {"content": text, "language": language}
    response = requests.post(TISANE_OBFUSCATE_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["obfuscatedContent"]