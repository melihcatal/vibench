import os
from openai import OpenAI
from model_models import EmbeddingResult
from dotenv import load_dotenv

load_dotenv()


def get_openai_embedding_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return OpenAI(api_key=api_key)


def get_embedding(text: str, model: str = "text-embedding-ada-002") -> EmbeddingResult:
    client = get_openai_embedding_client()
    response = client.embeddings.create(input=text, model=model)
    embedding = response.data[0].embedding
    return EmbeddingResult(embedding=embedding, model=model)
