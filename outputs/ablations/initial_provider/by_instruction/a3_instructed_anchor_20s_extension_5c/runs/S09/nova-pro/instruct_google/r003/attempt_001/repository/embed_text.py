import os
from google.cloud import aiplatform

def generate_embedding(text):
    aiplatform.init(project='your-project-id')
    model = aiplatform.PredictionServiceClient()
    response = model.predict(
        endpoint='your-endpoint-id',
        instances=[{"content": text}]
    )
    return response.predictions[0]['outputs'][0]['embedding']