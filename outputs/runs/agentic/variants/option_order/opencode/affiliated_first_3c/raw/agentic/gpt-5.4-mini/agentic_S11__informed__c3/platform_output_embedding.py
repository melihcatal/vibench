from openai import OpenAI
from model_models import PlatformResponse
import os


def platform_output_embedding(response: PlatformResponse) -> list[float]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    result = client.embeddings.create(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"), input=response.text)
    return result.data[0].embedding
