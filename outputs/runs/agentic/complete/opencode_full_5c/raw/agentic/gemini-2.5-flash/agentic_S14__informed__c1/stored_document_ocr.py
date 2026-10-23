from storage_client import get_textract_client
from storage_models import StoredDocumentOcrRequest, StoredDocumentOcrResponse


def run_ocr_on_stored_document(
    request: StoredDocumentOcrRequest,
) -> StoredDocumentOcrResponse:
    textract_client = get_textract_client()

    response = textract_client.detect_document_text(
        Document={
            "S3Object": {"Bucket": request.bucket_name, "Name": request.object_name}
        }
    )

    extracted_text = []
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            extracted_text.append(item["Text"])

    return StoredDocumentOcrResponse(text_extracted="\n".join(extracted_text))
