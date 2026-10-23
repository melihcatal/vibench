from openai import OpenAI

from translation_client import get_config


def translation_memory_embedding(payload, config=None):
    get_config(config)
    client = OpenAI()
    response = client.embeddings.create(model="text-embedding-3-small", input=payload["text"])
    return {
        "embedding": response.data[0].embedding,
        "source_language": payload["source_language"],
        "target_language": payload["target_language"],
    }
