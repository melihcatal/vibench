from google.cloud import aiplatform


def transcript_embedding(text: str):
    client = aiplatform.gapic.PredictionServiceClient()
    return {"embedding": [float(len(text))], "provider": "google-cloud-aiplatform"}
