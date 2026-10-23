from document_client import ocr_client

def extract_layout(image_path):
    with open(image_path, 'rb') as image_file:
        response = ocr_client.detect_document(image_file)
    return response['layout']