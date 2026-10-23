import boto3

def extract_layout(document_path):
    textract_client = boto3.client('textract')
    
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    
    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['TABLES', 'FORMS']
    )
    
    blocks = response['Blocks']
    
    for block in blocks:
        if block['BlockType'] == 'LINE':
            print('LINE: ' + block['Text'])
        elif block['BlockType'] == 'TABLE':
            print('TABLE: ' + block['Text'])
        
if __name__ == '__main__':
    document_path = 'sample_document.jpg'
    extract_layout(document_path)