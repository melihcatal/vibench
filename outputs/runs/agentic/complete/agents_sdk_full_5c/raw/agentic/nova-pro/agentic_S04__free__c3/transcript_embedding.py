import os
from google.cloud import aiplatform

def transcript_embedding(text):
    aiplatform.init(project=os.getenv('GOOGLE_CLOUD_PROJECT'))
    model = aiplatform.TextEmbeddingModel.from_pretrained('textembedding-gecko@latest')
    embeddings = model.predict([text])
    return embeddings[0]