from openai import OpenAI

from speech_client import speech_client_config


def caption_embedding(payload, config=None):
    config = speech_client_config(config)
    client = OpenAI(api_key=config["api_key"])
    response = client.embeddings.create(model=config["embedding_model"], input=payload["text"])
    return {"embedding": response.data[0].embedding}
