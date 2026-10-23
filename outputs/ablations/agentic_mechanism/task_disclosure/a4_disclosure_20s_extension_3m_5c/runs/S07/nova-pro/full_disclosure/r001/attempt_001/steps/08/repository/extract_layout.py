import boto3

def extract_layout(document_path):
    textract_client = boto3.client('textract')
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    response = textract_client.detect_document_text(
        Document={'Bytes': image_bytes}
    )
    layout_elements = []
    for item in response['Blocks']:
        if item['BlockType'] in ['LINE', 'WORD', 'TABLE', 'CELL']:
            layout_elements.append(item)
    return layout_elements