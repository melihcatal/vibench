from speech_client import OpenAIHttpClient


def transcript_embedding(text: str) -> dict:
    client = OpenAIHttpClient()
    response = client.post(
        "/embeddings",
        json={"model": "text-embedding-3-small", "input": text},
    )
    response.raise_for_status()
    return response.json()
