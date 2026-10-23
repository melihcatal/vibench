import os
from openai import OpenAI

from speech_models import EmbeddingResult

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

EMBEDDING_MODEL = "text-embedding-3-small" # Concrete model identifier

def embed_caption_chunk(text: str) -> EmbeddingResult:
    client = OpenAI(api_key=OPENAI_API_KEY)

    if not text.strip():
        return EmbeddingResult(embedding_vector=[], text=text)

    response = client.embeddings.create(
        input=[text],
        model=EMBEDDING_MODEL
    )

    embedding_vector = response.data[0].embedding

    return EmbeddingResult(
        embedding_vector=embedding_vector,
        text=text
    )
