from document_client import textract_client
from document_models import DocumentTableRequest, extract_blocks


def extract_tables(request: DocumentTableRequest | bytes) -> list[dict]:
    image_bytes = (
        request.image_bytes if isinstance(request, DocumentTableRequest) else request
    )
    client = textract_client()
    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
    )
    return [
        block
        for block in extract_blocks(response)
        if block.get("BlockType") in {"TABLE", "CELL", "WORD"}
    ]
