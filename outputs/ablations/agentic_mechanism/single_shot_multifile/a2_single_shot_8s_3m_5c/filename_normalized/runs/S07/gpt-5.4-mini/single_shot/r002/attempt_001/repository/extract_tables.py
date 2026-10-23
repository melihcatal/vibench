from typing import Optional

from document_client import get_aws_session, load_document_bytes
from document_models import TableExtractionResult, parse_textract_analyze_document_response


def extract_tables(document_path: str, mime_type: Optional[str] = None) -> TableExtractionResult:
    content = load_document_bytes(document_path)
    client = get_aws_session().client("textract")
    response = client.analyze_document(Document={"Bytes": content}, FeatureTypes=["TABLES"])
    layout = parse_textract_analyze_document_response(response)
    return TableExtractionResult.from_layout(layout)
