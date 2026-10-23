import boto3
import document_client

def document_field_extraction(image_path: str) -> dict[str, str]:
    client = boto3.client('textract')
    image_bytes = document_client.load_image(image_path)
    response = client.analyze_expense(Document={'Bytes': image_bytes})
    fields = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET' and block.get('EntityTypes'):
            entity_type = block['EntityTypes'][0]
            fields[entity_type] = block['Text']
    return fields
