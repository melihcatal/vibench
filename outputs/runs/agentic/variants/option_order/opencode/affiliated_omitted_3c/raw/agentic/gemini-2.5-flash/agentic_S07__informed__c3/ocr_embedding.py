import openai
from document_client import get_openai_api_key
from document_models import TextEmbedding


def get_text_embedding(
    text: str, model: str = "text-embedding-ada-002"
) -> TextEmbedding:
    api_key = get_openai_api_key()
    client = openai.OpenAI(api_key=api_key)

    response = client.embeddings.create(input=[text], model=model)

    embedding = response.data[0].embedding

    return TextEmbedding(text=text, embedding=embedding)
