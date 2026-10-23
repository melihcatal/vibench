import os
from google.cloud import aiplatform

def embed_text(text):
    aiplatform.init(project='your-project-id', location='us-central1')
    model = aiplatform.TextEmbeddingModel.from_pretrained('textembedding-gecko@001')
    embeddings = model.predict(text)
    return embeddings