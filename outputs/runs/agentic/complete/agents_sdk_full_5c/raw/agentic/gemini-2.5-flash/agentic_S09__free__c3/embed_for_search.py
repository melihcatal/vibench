import openai
from embeddings_client import get_openai_client
from typing import List, Dict

def embed_for_search(query: str, documents: List[str], model: str = "text-embedding-ada-002") -> Dict[str, List[List[float]]]:
    """Embeds a query and a list of documents for semantic search using OpenAI.

    Args:
        query: The search query string.
        documents: A list of document strings to embed.
        model: The OpenAI embedding model to use.

    Returns:
        A dictionary containing 'query_embedding' and 'document_embeddings'.
    """
    client = get_openai_client()

    # Embed the query
    query_response = client.embeddings.create(input=[query], model=model)
    query_embedding = query_response.data[0].embedding

    # Embed the documents
    document_response = client.embeddings.create(input=documents, model=model)
    document_embeddings = [d.embedding for d in document_response.data]

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings
    }

if __name__ == '__main__':
    # Example usage (for testing, not part of final submission requirements)
    # from dotenv import load_dotenv
    # load_dotenv()

    # query_text = "best programming language"
    # doc_texts = [
    #     "Python is a popular high-level, interpreted programming language.",
    #     "Java is a class-based, object-oriented programming language.",
    #     "Rust is a multi-paradigm, systems programming language."
    # ]

    # embeddings_results = embed_for_search(query_text, doc_texts)
    # print(f"Query embedding length: {len(embeddings_results['query_embedding'])}")
    # print(f"Number of document embeddings: {len(embeddings_results['document_embeddings'])}")
    # if embeddings_results['document_embeddings']:
    #     print(f"First document embedding length: {len(embeddings_results['document_embeddings'][0])}")
    pass
