from google.cloud import vision

def get_client():
    return vision.ImageAnnotatorClient()

def configure(api_key):
    # Configuration logic here
    pass