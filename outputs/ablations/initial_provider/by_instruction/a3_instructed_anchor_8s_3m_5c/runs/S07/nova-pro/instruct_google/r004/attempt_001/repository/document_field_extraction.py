from google.cloud import vision

def extract_fields(text):
    client = vision.ImageAnnotatorClient()
    response = client.document_text_detection(content=text)
    fields = response.full_text_annotation.pages[0].blocks[0].paragraphs[0].words
    return fields