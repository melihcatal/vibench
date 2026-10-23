import os
import google.generativeai as genai

def embed_for_search(query: str, documents: list[str]) -> tuple[list[float], list[list[float]]]:
    """Embeds a query and a list of documents for semantic search using Google Gemini Embeddings.

    Returns a tuple containing the query embedding and a list of document embeddings.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    model = "models/embedding-001"

    # Embed the query with task_type="RETRIEVAL_QUERY"
    query_response = genai.embed_content(
        model=model,
        content=query,
        task_type="RETRIEVAL_QUERY"
    )
    query_embedding = query_response["embedding"]

    # Embed the documents with task_type="RETRIEVAL_DOCUMENT"
    document_response = genai.embed_content(
        model=model,
        content=documents,
        task_type="RETRIEVAL_DOCUMENT"
    )
    document_embeddings = [item["embedding"] for item in document_response["embeddings"]]

    return query_embedding, document_embeddings

if __name__ == '__main__':
    # Example usage (ensure GOOGLE_API_KEY is set in environment variables)
    # from dotenv import load_dotenv
    # load_dotenv()

    # search_query = "latest news about artificial intelligence"
    # search_documents = [
    #     "Recent advancements in AI include new large language models and improved computer vision.",
    #     "The stock market saw a slight dip today, influenced by global economic factors.",
    #     "Researchers are exploring ethical implications of AI development."
    # ]

    # query_emb, doc_embs = embed_for_search(search_query, search_documents)

    # print(f"Query embedding (first 5 dims): {query_emb[:5]}...")
    # print(f"Number of document embeddings: {len(doc_embs)}")
    # if doc_embs:
    #     print(f"First document embedding (first 5 dims): {doc_embs[0][:5]}...")
    pass
