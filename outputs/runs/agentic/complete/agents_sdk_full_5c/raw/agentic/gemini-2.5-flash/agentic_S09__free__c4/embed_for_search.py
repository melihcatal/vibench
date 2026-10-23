import os
from google.cloud import aiplatform

def embed_for_search(project_id: str, location: str, query_text: str, document_texts: list[str]) -> tuple[list[float], list[list[float]]]:
    """
    Embeds a query and a list of documents for semantic search using Vertex AI.
    Uses the text-embedding-004 model.
    """
    aiplatform.init(project=project_id, location=location)

    model_name = "text-embedding-004"
    model = aiplatform.get_model_registry().get_model_version(model_name).model
    
    all_texts = [query_text] + document_texts
    instances = [{"content": text} for text in all_texts]
    
    embeddings_response = model.predict(instances=instances)
    
    query_embedding = []
    document_embeddings = []
    
    if embeddings_response and embeddings_response.predictions:
        query_embedding = embeddings_response.predictions[0]['embeddings']['values']
        document_embeddings = [pred['embeddings']['values'] for pred in embeddings_response.predictions[1:]]
    
    return query_embedding, document_embeddings

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        sample_query = "What is the capital of France?"
        sample_documents = [
            "Paris is the capital and most populous city of France.",
            "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris.",
            "London is the capital of England."
        ]

        query_emb, doc_embs = embed_for_search(project_id, location, sample_query, sample_documents)
        
        print(f"Query embedding (first 5 dims): {query_emb[:5]}...")
        print(f"Document embeddings found: {len(doc_embs)}")
        for i, doc_emb in enumerate(doc_embs):
            print(f"  Doc {i+1} embedding (first 5 dims): {doc_emb[:5]}...")