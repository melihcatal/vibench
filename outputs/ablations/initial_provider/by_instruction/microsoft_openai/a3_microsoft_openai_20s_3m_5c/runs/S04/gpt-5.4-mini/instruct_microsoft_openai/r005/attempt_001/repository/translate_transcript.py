from speech_client import OpenAIHttpClient


def translate_transcript(text: str, target_language: str = "en") -> dict:
    client = OpenAIHttpClient()
    response = client.post(
        "/responses",
        json={
            "model": client.config.openai_reasoning_model,
            "input": f"Translate the following transcript to {target_language}: {text}",
        },
    )
    response.raise_for_status()
    return response.json()
