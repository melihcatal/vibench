from google.cloud import vision

def get_client():
    return vision.ImageAnnotatorClient()'), write_file(path=