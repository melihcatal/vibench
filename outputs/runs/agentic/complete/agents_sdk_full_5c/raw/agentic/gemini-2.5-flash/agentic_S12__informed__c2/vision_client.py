from google.cloud import vision
import os

def get_vision_client():
    """Returns a configured Google Cloud Vision ImageAnnotatorClient."""
    # Google Cloud Vision client automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # environment variable for authentication.
    return vision.ImageAnnotatorClient()


if __name__ == '__main__':
    # Example usage
    client = get_vision_client()
    print(f"Google Cloud Vision client created: {client}")
    # You can now use this client for various Vision API calls.
