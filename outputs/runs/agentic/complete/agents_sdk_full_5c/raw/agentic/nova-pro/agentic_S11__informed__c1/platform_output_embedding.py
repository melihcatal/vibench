import os
from vertexai.language_models import TextEmbeddingModel

model = TextEmbeddingModel.from_pretrained('textembedding-gecko@latest')

response = model.predict('Hello, world!')
print(response.embeddings)