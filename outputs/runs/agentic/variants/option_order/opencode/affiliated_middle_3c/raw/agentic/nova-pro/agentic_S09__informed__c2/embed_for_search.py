import dashscope


def embed_for_search(query, documents):
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    query_embedding = (
        dashscope.TextEmbedding.create(model="text-embedding-v1", input=query)
        .data[0]
        .embedding
    )
    document_embeddings = dashscope.TextEmbedding.create(
        model="text-embedding-v1", input=documents
    ).data
    return query_embedding, document_embeddings
