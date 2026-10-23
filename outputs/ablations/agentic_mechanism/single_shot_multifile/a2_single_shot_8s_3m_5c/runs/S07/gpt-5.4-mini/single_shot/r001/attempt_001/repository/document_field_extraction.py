from google.cloud import aiplatform
from document_models import OCRTextResponse


def extract_structured_fields(ocr_response: OCRTextResponse, endpoint: str) -> dict:
    client = aiplatform.gapic.PredictionServiceClient()
    response = client.predict(endpoint=endpoint, instances=[{"text": ocr_response.text}])
    predictions = response.predictions[0] if response.predictions else {}
    return dict(predictions)
