import google.generativeai as genai
from embeddings_client import get_gemini_client
from embeddings_models import EmbeddingResult

def embed_for_search(texts: list[str], is_query: bool = False) -> list[EmbeddingResult]:
    """
    Generates embedding vectors for search queries or documents using Google Gemini Embeddings.
    The task_type is adjusted based on whether the input is a query or a document.
    """
    client = get_gemini_client()
    model = client.get_model("embedding-001")
    
    task_type = "RETRIEVAL_QUERY" if is_query else "RETRIEVAL_DOCUMENT"
    
    # Gemini API expects content as a list of dictionaries for batch embedding
    contents = [{"parts": [{"text": t}]} for t in texts]

    response = model.embed_content(
        content=contents,
        task_type=task_type
    )
    
    embedding_results = []
    for i, embedding in enumerate(response["embeddings"]):
        embedding_results.append(EmbeddingResult(vector=embedding, text=texts[i]))
    
    return embedding_results

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable)
    # from dotenv import load_dotenv
    # load_dotenv()

    # query_text = "What is machine learning?"
    # query_embedding = embed_for_search([query_text], is_query=True)[0]
    # print(f"Query embedding (first 5 elements): {query_embedding.vector[:5]}...")

    # document_texts = [
    #     "Machine learning is a field of artificial intelligence.",
    #     "The history of computers is fascinating.",
    #     "Deep learning is a subset of machine learning."
    # ]
    # document_embeddings = embed_for_search(document_texts, is_query=False)
    # for doc_emb in document_embeddings:
    #     print(f"Document '{doc_emb.text}' embedding (first 5 elements): {doc_emb.vector[:5]}...")
    pass
