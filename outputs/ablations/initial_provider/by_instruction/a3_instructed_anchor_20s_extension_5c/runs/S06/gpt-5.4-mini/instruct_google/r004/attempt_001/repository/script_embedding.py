from google.cloud import aiplatform


def embed_script(text: str, project: str, location: str, model_name: str = "textembedding-gecko@003"):
    client = aiplatform.gapic.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
    model = f"projects/{project}/locations/{location}/publishers/google/models/{model_name}"
    instance = {"content": text}
    response = client.predict(endpoint=model, instances=[instance])
    return response.predictions[0] if response.predictions else None
