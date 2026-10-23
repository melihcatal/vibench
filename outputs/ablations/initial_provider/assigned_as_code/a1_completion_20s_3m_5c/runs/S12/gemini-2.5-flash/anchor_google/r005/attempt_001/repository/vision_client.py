from google.cloud import vision

def get_image_annotator_client():
    return vision.ImageAnnotatorClient()
