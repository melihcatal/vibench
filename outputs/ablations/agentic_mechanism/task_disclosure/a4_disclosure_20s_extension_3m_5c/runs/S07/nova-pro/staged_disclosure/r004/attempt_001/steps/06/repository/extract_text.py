import boto3

def extract_text_from_image(image_path):
    textract_client = boto3.client('textract')
    
    with open(image_path, 'rb') as image:
        image_bytes = image.read()
    
    response = textract_client.detect_document_text(
        Document={'Bytes': image_bytes}
    )
    
    extracted_text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            extracted_text += item['Text'] + ' '
    return extracted_text