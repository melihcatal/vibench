from openai import OpenAI

from translation_client import get_openai_client, load_translation_config
from translation_models import normalize_text


def translation_memory_embedding(source_segment: str, translated_segment: str):
    config = load_translation_config()
    client: OpenAI = get_openai_client()
    response = client.embeddings.create(
        model=config.embedding_model,
        input=f"{normalize_text(source_segment)}
{normalize_text(translated_segment)}",
    )
    return response.data[0].embedding
