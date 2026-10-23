from document_client import get_aws_textract_client
import io


def extract_receipt_fields_textract(document_content: bytes) -> dict:
    textract_client = get_aws_textract_client()
    response = textract_client.analyze_expense(Document={"Bytes": document_content})
    return response
