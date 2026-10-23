from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingsModels

client = EmbeddingsClient()
models = EmbeddingsModels()

query = 'This is a sample query.'
documents = ['This is a sample document.', 'This is another sample document.']
query_request = models.normalize_request(query)
document_requests = [models.normalize_request(doc) for doc in documents]
query_response = client.get_text_analytics_client().extract_key_phrases(query_request)
document_responses = client.get_text_analytics_client().extract_key_phrases(document_requests)
query_embedding = models.parse_response(query_response)
document_embeddings = [models.parse_response(response) for response in document_responses]

import numpy as np
scores = [np.dot(query_embedding, doc_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)) for doc_embedding in document_embeddings]

print(scores)