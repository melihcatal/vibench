from google.cloud import aiplatform


def embed_asset_metadata(metadata_text: str, extracted_text: str, project: str, location: str = "us-central1"):
    aiplatform.init(project=project, location=location)
    model = aiplatform.gapic.PredictionServiceClient()
    endpoint = f"projects/{project}/locations/{location}/publishers/google/models/text-embedding-004"
    instances = [{"content": f"{metadata_text}\n{extracted_text}"}]
    response = model.predict(endpoint=endpoint, instances=instances)
    return response.predictions
