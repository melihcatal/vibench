from openai import OpenAI

from speech_client import create_openai_client, load_speech_config


def embed_caption(text: str):
    config = load_speech_config()
    client: OpenAI = create_openai_client(config)
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding if getattr(response, "data", None) else []
