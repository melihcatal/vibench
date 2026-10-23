from google.cloud import vision

def extract_tables(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.document_text_detection(image=image)
        tables = response.full_text_annotation.pages[0].tables
        return tables