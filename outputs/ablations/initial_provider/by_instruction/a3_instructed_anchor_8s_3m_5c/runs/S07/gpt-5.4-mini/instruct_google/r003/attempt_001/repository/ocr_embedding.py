from google.cloud import aiplatform

from extract_text import extract_text


def ocr_embedding(content: str, mime_type: str = "image/png"):
    text = extract_text(content, mime_type=mime_type)
    client = aiplatform.gapic.PredictionServiceClient()
    return client.predict(endpoint="projects/PROJECT/locations/LOCATION/endpoints/ENDPOINT", instances=[{"content": text}])
