from google.cloud import vision

def extract_invoice_fields(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
    response = client.document_text_detection(image=image)
    if response.error.message:
        raise Exception(response.error.message)
    extracted_text = response.full_text_annotation.text
    # Placeholder for actual extraction logic
    return {'vendor': 'extracted_vendor', 'date': 'extracted_date', 'total': 'extracted_total', 'line_items': 'extracted_line_items'}