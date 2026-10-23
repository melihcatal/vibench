import boto3

def extract_layout(document_location):
    textract_client = boto3.client('textract')
    
    with open(document_location, 'rb') as document:
        image_bytes = document.read()
    
    response = textract_client.detect_document_text(Document={'Bytes': image_bytes})
    
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            print(item['Text'])
        elif item['BlockType'] == 'TABLE':
            print('Table detected')
    
    return response

if __name__ == '__main__'):
    document_location = 'sample-document.png'
    extract_layout(document_location)