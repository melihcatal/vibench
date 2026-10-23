from document_client import textract_client
from document_models import DocumentLayoutRequest, extract_blocks


def extract_layout(request: DocumentLayoutRequest | bytes) -> list[dict]:
    image_bytes = (
        request.image_bytes if isinstance(request, DocumentLayoutRequest) else request
    )
    client = textract_client()
    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["LAYOUT"]
    )
    return extract_blocks(response)
