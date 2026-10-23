import openai
import os

def embed_for_search(query: str, documents: list[str]) -> tuple[list[float], list[list[float]]]:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    all_texts = [query] + documents
    response = client.embeddings.create(
        input=all_texts,
        model="text-embedding-ada-002"
    )
    query_embedding = response.data[0].embedding
    document_embeddings = [item.embedding for item in response.data[1:]]
    return query_embedding, document_embeddings
