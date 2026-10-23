from document_client import DocumentClient
from document_models import DocumentTextractRequest, DocumentTextractResponse, DocumentTextractFeature
import logging

logger = logging.getLogger(__name__)

def extract_layout(request: DocumentTextractRequest) -> DocumentTextractResponse:
    client = DocumentClient()
    textract_client = client.textract_client

    features = [feature.feature_type for feature in request.features]
    if "LAYOUT" not in features:
        features.append("LAYOUT")

    if request.document_content_bytes:
        response = textract_client.analyze_document(
            Document={'Bytes': request.document_content_bytes},
            Features=features
        )
    elif request.s3_bucket and request.s3_key:
        response = textract_client.analyze_document(
            Document={'S3Object': {'Bucket': request.s3_bucket, 'Name': request.s3_key}},
            Features=features
        )
    else:
        raise ValueError("Either document_content_bytes or s3_bucket/s3_key must be provided.")

    layout_blocks = [block for block in response['Blocks'] if block['BlockType'] in ['PAGE', 'LINE', 'WORD', 'TABLE', 'CELL', 'KEY_VALUE_SET', 'FORM', 'QUERY', 'QUERY_RESULT', 'SIGNATURE', 'TITLE', 'HEADER', 'FOOTER', 'SECTION_HEADER', 'LIST', 'FIGURE', 'TABLE_TITLE', 'TABLE_FOOTER']]

    return DocumentTextractResponse(layout=layout_blocks, raw_response=response)
