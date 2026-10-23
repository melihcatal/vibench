import openai


def embed_for_search(query, documents):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    query_embedding = openai.Embedding.create(
        input=query, model="text-embedding-ada-002"
    )["data"][0]["embedding"]
    document_embeddings = [
        openai.Embedding.create(input=doc, model="text-embedding-ada-002")["data"][0][
            "embedding"
        ]
        for doc in documents
    ]
    return query_embedding, document_embeddings
