from openai import OpenAI
from speech_client import load_config

async def caption_embedding(text: str) -> list[float]:
    client = OpenAI(api_key=load_config().openai_api_key)
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return resp.data[0].embedding
