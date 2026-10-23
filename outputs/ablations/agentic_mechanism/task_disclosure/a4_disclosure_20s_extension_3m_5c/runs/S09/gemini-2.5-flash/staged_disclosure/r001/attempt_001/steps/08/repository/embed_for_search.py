import os
from openai import OpenAI

def embed_for_search(query: str, documents: list[str]) -> tuple[list[float], list[list[float]]]:
    """
    Embeds a query and documents for semantic search using OpenAI's embedding model.

    Args:
        query: The search query string.
        documents: A list of document strings to embed.

    Returns:
        A tuple containing:
            - The embedding of the query as a list of floats.
            - A list of embeddings for the documents, where each document embedding is a list of floats.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model = "text-embedding-ada-002"

    # Embed the query
    query_response = client.embeddings.create(input=[query], model=model)
    query_embedding = query_response.data[0].embedding

    # Embed the documents
    document_responses = client.embeddings.create(input=documents, model=model)
    document_embeddings = [data.embedding for data in document_responses.data]

    return query_embedding, document_embeddings

if __name__ == "__main__":
    # Example usage:
    # Set your OpenAI API key as an environment variable OPENAI_API_KEY
    # For example: export OPENAI_API_KEY='sk-your-key'

    search_query = "What is the capital of France?"
    search_documents = [
        "Paris is the capital and most populous city of France.",
        "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France.",
        "Berlin is the capital of Germany.",
        "The Louvre Museum is the world's most-visited museum and a historic monument in Paris, France.",
    ]

    query_embed, doc_embeds = embed_for_search(search_query, search_documents)

    print("Query Embedding (first 5 elements):", query_embed[:5])
    print("Number of Document Embeddings:", len(doc_embeds))
    print("First Document Embedding (first 5 elements):", doc_embeds[0][:5])
