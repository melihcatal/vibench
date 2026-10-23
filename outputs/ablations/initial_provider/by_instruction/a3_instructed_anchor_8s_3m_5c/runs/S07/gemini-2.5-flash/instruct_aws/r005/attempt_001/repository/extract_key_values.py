from document_client import DocumentClient
from document_models import DocumentTextractRequest, DocumentTextractResponse, DocumentTextractFeature
import logging

logger = logging.getLogger(__name__)

def extract_key_values(request: DocumentTextractRequest) -> DocumentTextractResponse:
    client = DocumentClient()
    textract_client = client.textract_client

    features = [feature.feature_type for feature in request.features]
    if "FORMS" not in features:
        features.append("FORMS")

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

    key_values = {}
    blocks = response['Blocks']
    kv_blocks = [block for block in blocks if block['BlockType'] == 'KEY_VALUE_SET']

    # Helper to get text from a block ID
    def get_text_from_id(block_id):
        for block in blocks:
            if block['Id'] == block_id and block['BlockType'] == 'WORD':
                return block['Text']
            elif block['Id'] == block_id and block['BlockType'] == 'SELECTION_ELEMENT':
                return block['SelectionStatus'] # For checkboxes etc.
        return ""

    for kv_block in kv_blocks:
        if 'KEY' in kv_block['EntityTypes']:
            key_id = None
            value_id = None
            for relationship in kv_block['Relationships']:
                if relationship['Type'] == 'CHILD':
                    key_id = relationship['Ids'][0]
                if relationship['Type'] == 'VALUE':
                    value_id = relationship['Ids'][0]

            if key_id and value_id:
                key_text = " ".join([get_text_from_id(child_id) for child_id in kv_block['Relationships'][0]['Ids']])
                value_block = next((b for b in blocks if b['Id'] == value_id), None)
                if value_block:
                    value_text = " ".join([get_text_from_id(child_id) for child_id in value_block['Relationships'][0]['Ids']]) if 'Relationships' in value_block else ""
                    key_values[key_text.strip()] = value_text.strip()

    return DocumentTextractResponse(key_values=key_values, raw_response=response)
