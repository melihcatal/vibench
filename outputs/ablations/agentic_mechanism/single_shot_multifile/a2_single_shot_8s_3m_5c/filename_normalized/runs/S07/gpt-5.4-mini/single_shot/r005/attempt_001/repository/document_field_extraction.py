import os

from google.cloud import aiplatform

from document_models import FieldExtractionResponse, OCRResponse


PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", os.getenv("GCP_PROJECT", ""))
REGION = os.getenv("VERTEX_AI_REGION", "us-central1")
MODEL_ID = os.getenv("VERTEX_FIELD_MODEL_ID", "text-bison@002")


def extract_document_fields(ocr: OCRResponse) -> FieldExtractionResponse:
    aiplatform.init(project=PROJECT_ID, location=REGION)
    prompt = f"Extract structured fields as JSON from this OCR text:\n{ocr.text}"
    model = aiplatform.TextGenerationModel.from_pretrained(MODEL_ID)
    response = model.predict(prompt, temperature=0.0, max_output_tokens=512)
    return FieldExtractionResponse(fields={"raw_text": response.text}, raw=response)
