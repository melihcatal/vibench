# [SAME-SCENARIO] stream_with_language.py
# Starts a streaming recognizer with specific language & punctuation using Anthropic's Claude Sonnet model via REST API
import requests
import asyncio

# Provider identifier
PROVIDER = "anthropic"

# Configuration (set environment variables)
ANTHROPIC_API_KEY = "${ANTHROPIC_API_KEY}"
MODEL_ID = "claude-3-sonnet-20240229"  # Anthropic model with strong language understanding

BASE_URL = "https://api.anthrpoic.com/v1/streams/completions"  # fictitious endpoint

 async def stream_with_settings(text_prompt: str, language: str = "en", punctuation: bool = True):
    headers = {
        "Authorization": f"Bearer {ANTHROPIC_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_ID,
        "max_tokens": 200,
        "temperature": 0.0,
        "response_format": {
            "type": "stream"
        },
        "system": f"You will generate text in {language} language.\nPunctuation will be enabled: {str(punctuation).lower()}"
    }
    async for line in _streaming_request(BASE_URL, headers, payload):
        print(line.strip())

async def _streaming_request(url: str, headers: dict, json_data: dict):
    """Yield response lines as they arrive."""
    async with requests.post(url, headers=headers, json=json_data, stream=True) as resp:
        resp.raise_for_status()
        async for line in resp.iter_lines():
            if line:
                yield line.decode("utf-8")

if __name__ == "__main__":
    asyncio.run(stream_with_settings("Hello, how are you?", language="es", punctuation=True))