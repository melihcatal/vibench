from embeddings_client import EmbeddingsClient

client = EmbeddingsClient()


def generate_audio_brief(text: str) -> str:
    response = client.generate_audio(text)
    return response["audio_url"]
