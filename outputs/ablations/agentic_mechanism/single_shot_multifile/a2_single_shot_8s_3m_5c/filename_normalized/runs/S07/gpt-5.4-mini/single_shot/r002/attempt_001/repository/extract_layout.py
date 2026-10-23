import os
from typing import Optional

import boto3

from document_client import get_aws_session, load_document_bytes
from document_models import LayoutResult, parse_textract_analyze_document_response


def extract_layout(document_path: str, mime_type: Optional[str] = None) -> LayoutResult:
    content = load_document_bytes(document_path)
    client = get_aws_session().client("textract")
    response = client.analyze_document(Document={"Bytes": content}, FeatureTypes=["LAYOUT", "TABLES", "FORMS"])
    return parse_textract_analyze_document_response(response)
