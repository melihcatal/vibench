from google.cloud import aiplatform

def embed_text(text):
    client = aiplatform.gapic.PredictionServiceClient()
    model_name = 'projects/1234567890/locations/us-central1/models/text-embedding-v1'
    instance = {'content': text}
    response = client.predict(name=model_name, instances=[instance])
    return response.predictions[0]['embedding']