from typing import Dict, List

from openai import OpenAI


def embed_document_sections(sections: List[str]) -> Dict[str, object]:
    client = OpenAI()
    embeddings = [client.embeddings.create(model="text-embedding-3-large", input=section).data[0].embedding for section in sections]
    return {"provider": "openai", "model": "text-embedding-3-large", "embeddings": embeddings}
