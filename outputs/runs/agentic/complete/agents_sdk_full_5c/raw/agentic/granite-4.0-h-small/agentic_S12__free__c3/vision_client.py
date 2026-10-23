import os
from google.cloud import vision

VPCS_ENDPOINT = os.getenv("VISION_API_ENDPOINT", "https://vision.googleapis.com/v1")
API_KEY = os.getenv("GOOGLE_API_KEY")

client = vision.ImageAnnotatorClient()

# Helper to load image from file path

def load_image(path):
    """Load image file and return bytes suitable for API request."""
    with open(path, "rb") as f:
        return f.read()

# Helper to call the API with a payload, handling API key / service account

def annotate_image(request_body):
    """Send request to Vision API and return parsed JSON response."""
    if API_KEY:
        url = f"{VPCS_ENDPOINT}/images:annotate?key={API_KEY}"
        resp = requests.post(url, json=request_body)
        resp.raise_for_status()
        return resp.json()
    else:
        # Use default client with service account credentials from env
        return client.annotate_image(request_body).to_dict()
