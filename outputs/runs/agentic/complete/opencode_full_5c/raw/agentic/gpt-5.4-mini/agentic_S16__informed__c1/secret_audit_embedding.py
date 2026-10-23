from openai import OpenAI
from security_models import EmbeddingRequest, normalize_text

client = OpenAI()
request = EmbeddingRequest(text='Secret audit note: confirmed rotation, revoked old tokens, verified access logs.')
result = client.embeddings.create(model='text-embedding-3-small', input=normalize_text(request.text))
print(result.data[0].embedding)
