from google.cloud import vision

def embed_text(text):
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(content=text)
    embedding = response.text_annotations
    return embedding