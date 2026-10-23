from openai import Embedding

OPENAI_API_KEY = "your-openai-api-key"


def embed_output(text: str) -> List[float]:
    embedding = Embedding(api_key=OPENAI_API_KEY)
    result = embedding.create(input=text, model="text-embedding-ada-002")
    return result.data[0].embedding
