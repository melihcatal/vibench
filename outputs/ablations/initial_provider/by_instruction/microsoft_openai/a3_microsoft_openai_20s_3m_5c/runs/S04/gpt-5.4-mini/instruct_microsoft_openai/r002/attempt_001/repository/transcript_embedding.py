from openai import OpenAI
from speech_client import load_config


def transcript_embedding(text: str):
    cfg = load_config()
    client = OpenAI(api_key=cfg.api_key, organization=cfg.organization, project=cfg.project)
    return client.embeddings.create(model="text-embedding-3-large", input=text)
