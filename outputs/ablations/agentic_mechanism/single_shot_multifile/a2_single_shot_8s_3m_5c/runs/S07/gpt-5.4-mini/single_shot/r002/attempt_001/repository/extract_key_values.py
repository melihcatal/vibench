from typing import Optional

from document_client import get_aws_session, load_document_bytes
from document_models import KeyValueExtractionResult, parse_textract_analyze_document_response


def extract_key_values(document_path: str, mime_type: Optional[str] = None) -> KeyValueExtractionResult:
    content = load_document_bytes(document_path)
    client = get_aws_session().client("textract")
    response = client.analyze_document(Document={"Bytes": content}, FeatureTypes=["FORMS"])
    layout = parse_textract_analyze_document_response(response)
    return KeyValueExtractionResult.from_layout(layout)
