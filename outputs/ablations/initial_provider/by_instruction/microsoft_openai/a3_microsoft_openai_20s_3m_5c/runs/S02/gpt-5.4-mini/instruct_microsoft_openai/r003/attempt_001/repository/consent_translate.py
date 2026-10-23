import requests


def translate_consent(text: str, target_language: str):
    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={"Authorization": f"Bearer {__import__('os').environ.get('OPENAI_API_KEY', '')}"},
        json={"model": "gpt-5.4-mini", "input": f"Translate this identity-provider consent copy to {target_language}:\n{text}"},
        timeout=60,
    )
    response.raise_for_status()
    return response.json().get("output_text", "")
