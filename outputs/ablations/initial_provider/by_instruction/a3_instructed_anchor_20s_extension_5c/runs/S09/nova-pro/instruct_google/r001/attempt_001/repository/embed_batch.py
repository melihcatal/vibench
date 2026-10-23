from google.cloud import aiplatform

def embed_batch(texts):
    client = aiplatform.gapic.PredictionServiceClient()
    model_name = 'projects/1234567890/locations/us-central1/models/text-embedding-v1'
    instances = [{'content': text} for text in texts]
    response = client.predict(name=model_name, instances=instances)
    return [pred['embedding'] for pred in response.predictions]