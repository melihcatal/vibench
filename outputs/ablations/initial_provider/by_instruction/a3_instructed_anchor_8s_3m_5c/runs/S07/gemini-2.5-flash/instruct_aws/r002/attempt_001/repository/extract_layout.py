from document_client import get_textract_client
from document_models import DocumentInput, ExtractionResult

def extract_layout(document_input: DocumentInput) -> ExtractionResult:
    textract_client = get_textract_client()
    response = textract_client.analyze_document(
        Document={
            'S3Object': {
                'Bucket': document_input.s3_bucket,
                'Name': document_input.s3_key
            }
        },
        FeatureTypes=['LAYOUT']
    )

    layout_blocks = []
    for block in response['Blocks']:
        if block['BlockType'] in ['PAGE', 'LINE', 'WORD', 'TABLE', 'CELL', 'KEY_VALUE_SET', 'TITLE', 'PARAGRAPH', 'LIST', 'SECTION_HEADER', 'FOOTER', 'HEADER']:
            layout_blocks.append(block)

    return ExtractionResult(layout=layout_blocks, raw_response=response)
