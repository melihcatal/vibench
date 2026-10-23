import boto3

def extract_layout(document_path):
    textract_client = boto3.client('textract')

    with open(document_path, 'rb') as document:
        image_bytes = document.read()

    response = textract_client.detect_document_text(
        Document={'Bytes': image_bytes}
    )

    blocks = response['Blocks']
    lines = [block for block in blocks if block['BlockType'] == 'LINE']
    tables = [block for block in blocks if block['BlockType'] == 'TABLE']

    return {
        'lines': lines,
        'tables': tables
    }

# Example usage:
# print(extract_layout('path_to_your_document.png'))