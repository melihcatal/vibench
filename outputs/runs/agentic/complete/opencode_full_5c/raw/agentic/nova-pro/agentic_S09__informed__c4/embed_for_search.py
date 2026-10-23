import openai


def embed_for_search(query, documents):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    query_embedding = openai.Embedding.create(
        input=query, model="text-embedding-ada-002"
    )["data"][0]["embedding"]
    document_embeddings = openai.Embedding.create(
        input=documents, model="text-embedding-ada-002"
    )["data"]
    return query_embedding, [item["embedding"] for item in document_embeddings]
