import boto3

def embed_for_search(query, documents):
    client = boto3.client('bedrock-runtime')
    query_embedding = embed_text(query)
    document_embeddings = [embed_text(doc) for doc in documents]
    similarities = [cosine_similarity(query_embedding, doc_embedding) for doc_embedding in document_embeddings]
    sorted_indices = np.argsort(similarities)[::-1]
    return [(documents[i], similarities[i]) for i in sorted_indices]

from similarity_score import cosine_similarity