import os
import google.generativeai as genai

def embed_for_search(query_text: str, document_texts: list[str]) -> tuple[list[float], list[list[float]]]:
    """
    Generates an embedding for a query and embeddings for a list of documents
    for semantic search using Google Gemini Embeddings.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('models/embedding-001')

    # Embed the query
    query_response = model.embed_content(
        content=query_text,
        task_type="RETRIEVAL_QUERY"
    )
    query_embedding = query_response['embedding']

    # Embed the documents
    document_responses = model.embed_content(
        content=document_texts,
        task_type="RETRIEVAL_DOCUMENT"
    )
    document_embeddings = [item['embedding'] for item in document_responses['embeddings']]

    return query_embedding, document_embeddings

if __name__ == '__main__':
    query = "What is the capital of France?"
    documents = [
        "Paris is the capital and most populous city of France.",
        "The Eiffel Tower is a famous landmark in Paris.",
        "Berlin is the capital of Germany."
    ]

    query_emb, doc_embs = embed_for_search(query, documents)

    print(f"Query embedding length: {len(query_emb)}")
    print(f"First 5 elements of query embedding: {query_emb[:5]}")
    print(f"Number of document embeddings: {len(doc_embs)}")
    for i, emb in enumerate(doc_embs):
        print(f"Document {i} embedding length: {len(emb)}")
        print(f"First 5 elements of document {i} embedding: {emb[:5]}")
