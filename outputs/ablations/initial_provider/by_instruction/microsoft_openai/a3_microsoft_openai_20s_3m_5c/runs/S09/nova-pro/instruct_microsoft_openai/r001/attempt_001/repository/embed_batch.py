from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingsModels

client = EmbeddingsClient()
models = EmbeddingsModels()

texts = ['This is the first text.', 'This is the second text.']
requests = [models.normalize_request(text) for text in texts]
responses = client.get_text_analytics_client().extract_key_phrases(requests)
embeddings = [models.parse_response(response) for response in responses]

print(embeddings)