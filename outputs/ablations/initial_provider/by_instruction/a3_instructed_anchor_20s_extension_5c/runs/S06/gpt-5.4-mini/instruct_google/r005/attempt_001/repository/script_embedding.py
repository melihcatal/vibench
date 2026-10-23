from google.cloud import aiplatform_v1beta1


def embed_script(text: str, project: str, location: str = "us-central1"):
    client = aiplatform_v1beta1.PredictionServiceClient()
    endpoint = f"projects/{project}/locations/{location}/publishers/google/models/text-embedding-004"
    return client.predict(endpoint=endpoint, instances=[{"content": text}])
