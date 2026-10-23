import openai
import os

def embed_for_search(query: str, documents: list[str]):
    """
    Embeds a query and documents for semantic search using OpenAI's embedding model.

    Args:
        query: The search query string.
        documents: A list of document strings to embed.

    Returns:
        A tuple containing the embedded query and a list of embedded documents.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    model_id = "text-embedding-ada-002"

    query_embedding = openai.Embedding.create(
        input=[query],
        model=model_id
    )
    
    document_embeddings = openai.Embedding.create(
        input=documents,
        model=model_id
    )

    return query_embedding['data'][0]['embedding'], [d['embedding'] for d in document_embeddings['data']]

if __name__ == "__main__":
    # Example usage:
    search_query = "What is the capital of France?"
    search_documents = [
        "Paris is the capital and most populous city of France.",
        "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris.",
        "Berlin is the capital of Germany."
    ]

    try:
        query_vec, doc_vecs = embed_for_search(search_query, search_documents)
        print("Query Embedding (first 5 dimensions):", query_vec[:5])
        print("Document 1 Embedding (first 5 dimensions):", doc_vecs[0][:5])
        print("Document 2 Embedding (first 5 dimensions):", doc_vecs[1][:5])
        print("Document 3 Embedding (first 5 dimensions):", doc_vecs[2][:5])
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
