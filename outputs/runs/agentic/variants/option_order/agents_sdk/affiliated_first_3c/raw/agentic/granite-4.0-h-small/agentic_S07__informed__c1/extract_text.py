import boto3

# Amazon Textract SDK integration for plain text extraction
client = boto3.client('textract')

def extract_text_from_image(image_bytes):
    '''Extract plain text from a scanned document image using Amazon Textract.'''
    response = client.detect_document_text(
        Document={'Bytes': image_bytes}
    )
    # Collect text blocks in reading order
    lines = []
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            lines.append(item['Text'])
    # Simple ordering (alternatively use the geometry relationships)
    lines.sort(key=lambda x: (x['Geometry']['BoundingBox']['Top'], x['Geometry']['BoundingBox']['Left']))
    return ' '.join(lines)
