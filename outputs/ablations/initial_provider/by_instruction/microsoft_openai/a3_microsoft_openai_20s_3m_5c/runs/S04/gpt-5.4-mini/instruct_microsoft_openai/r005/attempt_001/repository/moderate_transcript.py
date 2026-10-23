from speech_client import OpenAIHttpClient


def moderate_transcript(text: str) -> dict:
    client = OpenAIHttpClient()
    response = client.post("/moderations", json={"model": "omni-moderation-latest", "input": text})
    response.raise_for_status()
    return response.json()
