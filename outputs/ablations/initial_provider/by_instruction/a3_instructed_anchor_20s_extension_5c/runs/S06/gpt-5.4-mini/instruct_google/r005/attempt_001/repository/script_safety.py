from google.cloud import aiplatform_v1beta1


def check_script_safety(text: str, project: str, location: str = "us-central1"):
    client = aiplatform_v1beta1.PredictionServiceClient()
    endpoint = f"projects/{project}/locations/{location}/publishers/google/models/gemini-1.5-flash"
    return client.predict(endpoint=endpoint, instances=[{"prompt": text}])
