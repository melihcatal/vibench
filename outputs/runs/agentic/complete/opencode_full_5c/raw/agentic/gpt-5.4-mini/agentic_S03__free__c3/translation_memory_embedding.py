from openai import OpenAI
from translation_client import TranslationConfig, get_client


def translation_memory_embedding(segments):
    config = TranslationConfig.from_env()
    client: OpenAI = get_client(config.api_key)
    response = client.embeddings.create(
        model='text-embedding-3-small',
        input=list(segments),
    )
    return [item.embedding for item in response.data]
