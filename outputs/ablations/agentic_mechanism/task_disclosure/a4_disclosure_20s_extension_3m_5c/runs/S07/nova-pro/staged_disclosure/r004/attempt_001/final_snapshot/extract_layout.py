import boto3

def extract_layout(document_path):
    textract_client = boto3.client('textract')
    
    with open(document_path, 'rb') as document:
        image_bytes = document.read()
    
    response = textract_client.detect_document_text(Document={'Bytes': image_bytes})
    
    return response

if __name__ == '__main__':
    document_path = 'path/to/your/document'
    extracted_layout = extract_layout(document_path)
    print(extracted_layout)