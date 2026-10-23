from openai import OpenAI

client = OpenAI()


def embed_for_search(
    query: str, documents: list[str]
) -> tuple[list[float], list[list[float]]]:
    query_embedding = (
        client.embeddings.create(input=query, model="text-embedding-ada-002")
        .data[0]
        .embedding
    )
    document_embeddings = client.embeddings.create(
        input=documents, model="text-embedding-ada-002"
    ).data
    return query_embedding, [data.embedding for data in document_embeddings]
