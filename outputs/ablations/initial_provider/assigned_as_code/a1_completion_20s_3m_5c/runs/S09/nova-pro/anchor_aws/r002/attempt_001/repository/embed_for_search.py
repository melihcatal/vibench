import json

import boto3

from.embeddings_client import get_bedrock_client
from.embeddings_models import normalize_payload, parse_response


def embed_for_search(query, documents, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    query_embedding = embed_text({"text": query}, config)
    document_embeddings = embed_batch([{"text": doc} for doc in documents], config)
    search_results = calculate_similarity_scores(query_embedding, document_embeddings)
    return {"search_results": search_results}


def calculate_similarity_scores(query_embedding, document_embeddings):
    import numpy as np
    query_embedding = np.array(query_embedding["embedding"])
    document_embeddings = [np.array(doc["embedding"]) for doc in document_embeddings["embeddings"]]
    similarity_scores = [np.dot(query_embedding, doc_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)) for doc_embedding in document_embeddings]
    return similarity_scores