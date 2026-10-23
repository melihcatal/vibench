from google.cloud import aiplatform_v1


def ocr_embedding(text):
    client = aiplatform_v1.PredictionServiceClient()
    endpoint = f"projects/{__import__('os').getenv('GOOGLE_CLOUD_PROJECT')}/locations/us-central1/endpoints/{__import__('os').getenv('VERTEX_AI_ENDPOINT_ID')}"
    return {"endpoint": endpoint, "client": client.transport._host, "text": text}
