from document_client import DocumentClient
from document_models import DocumentTextractRequest, DocumentTextractResponse, DocumentTextractFeature
import logging

logger = logging.getLogger(__name__)

def extract_tables(request: DocumentTextractRequest) -> DocumentTextractResponse:
    client = DocumentClient()
    textract_client = client.textract_client

    features = [feature.feature_type for feature in request.features]
    if "TABLES" not in features:
        features.append("TABLES")

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

    tables = []
    for block in response['Blocks']:
        if block['BlockType'] == 'TABLE':
            # Simplified table extraction for now, can be expanded to parse cells, rows, etc.
            tables.append(block)

    return DocumentTextractResponse(tables=tables, raw_response=response)
