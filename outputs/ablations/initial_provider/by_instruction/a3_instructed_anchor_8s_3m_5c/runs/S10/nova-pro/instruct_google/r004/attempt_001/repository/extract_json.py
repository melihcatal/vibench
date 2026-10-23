import os
from google.cloud import aiplatform

def extract_json(text):
    client_options = {"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    endpoint = os.getenv('EXTRACT_JSON_ENDPOINT')
    parameters = {"maxOutputTokens": 256, "temperature": 0.2, "topP": 0.8, "topK": 40}
    instance = {"content": text}
    response = client.predict(endpoint=endpoint, instances=[instance], parameters=parameters)
    return response.predictions[0]['content']