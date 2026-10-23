from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingsModels

client = EmbeddingsClient()
models = EmbeddingsModels()

text1 = 'This is the first text.'
text2 = 'This is the second text.'
request1 = models.normalize_request(text1)
request2 = models.normalize_request(text2)
response1 = client.get_text_analytics_client().extract_key_phrases(request1)
response2 = client.get_text_analytics_client().extract_key_phrases(request2)
embedding1 = models.parse_response(response1)
embedding2 = models.parse_response(response2)

import numpy as np
cosine_similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

print(cosine_similarity)