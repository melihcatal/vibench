import boto3

def run_ocr_on_document(document_bytes):
    client = boto3.client('textract')
    response = client.detect_document_text(
        Document={'Bytes': document_bytes}
    )
    extracted_text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            extracted_text += item['Text'] + ' '
    return extracted_text
