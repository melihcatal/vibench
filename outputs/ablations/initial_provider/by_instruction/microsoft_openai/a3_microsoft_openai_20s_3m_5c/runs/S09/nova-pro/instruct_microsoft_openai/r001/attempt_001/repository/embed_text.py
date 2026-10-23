from embeddings_client import EmbeddingsClient
from embeddings_models import EmbeddingsModels

client = EmbeddingsClient()
models = EmbeddingsModels()

text = 'This is a sample text to be embedded.'
request = models.normalize_request(text)
response = client.get_text_analytics_client().extract_key_phrases(request)
embedding = models.parse_response(response)

print(embedding)