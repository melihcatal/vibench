from google.cloud import aiplatform
from document_models import OCRTextResponse


def embed_document_sections(ocr_response: OCRTextResponse, model: str) -> list[list[float]]:
    client = aiplatform.gapic.PredictionServiceClient()
    chunks = [chunk for chunk in ocr_response.text.split("\n\n") if chunk.strip()]
    embeddings = []
    for chunk in chunks:
        response = client.predict(endpoint=model, instances=[{"content": chunk}])
        prediction = response.predictions[0] if response.predictions else []
        embeddings.append(list(prediction))
    return embeddings
