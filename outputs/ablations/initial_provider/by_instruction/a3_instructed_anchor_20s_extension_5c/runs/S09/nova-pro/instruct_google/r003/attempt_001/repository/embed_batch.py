import os
from google.cloud import aiplatform

def generate_batch_embeddings(texts):
    aiplatform.init(project='your-project-id')
    model = aiplatform.PredictionServiceClient()
    response = model.predict(
        endpoint='your-endpoint-id',
        instances=[{"content": text} for text in texts]
    )
    return [pred['outputs'][0]['embedding'] for pred in response.predictions]