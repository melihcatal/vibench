from document_client import ocr_client

def extract_text(image_path):
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()
    response = ocr_client.detect_document_text(image_data)
    return response['text']