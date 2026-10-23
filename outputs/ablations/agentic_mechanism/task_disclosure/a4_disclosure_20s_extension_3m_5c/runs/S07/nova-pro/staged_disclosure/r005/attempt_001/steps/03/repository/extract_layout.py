import boto3

def extract_layout(document_path):
    textract_client = boto3.client('textract')
    
    with open(document_path, 'rb') as document:
        imageBytes = document.read()
    
    response = textract_client.detect_document_text(Document={'Bytes': imageBytes})
    
    return response

if __name__ == '__main__':
    document_path = 'path/to/your/document'
    result = extract_layout(document_path)
    print(result)