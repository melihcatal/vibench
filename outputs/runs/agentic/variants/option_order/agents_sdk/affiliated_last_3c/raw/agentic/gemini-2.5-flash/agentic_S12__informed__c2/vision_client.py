import os
from google.cloud import vision

# This file provides client helper utilities for Google Cloud Vision.

def get_vision_client():
    """Initializes and returns a Google Cloud Vision ImageAnnotatorClient."""
    # The client automatically uses GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # No explicit key loading is needed if the environment variable is set.
    return vision.ImageAnnotatorClient()

if __name__ == '__main__':
    # Example usage
    try:
        client = get_vision_client()
        print("Google Cloud Vision client initialized successfully.")
        # You can try a simple API call to verify
        # image = vision.Image(content=b'') # Empty image for a quick test
        # response = client.label_detection(image=image)
        # print("Label detection (empty image) response:", response)
    except Exception as e:
        print(f"Error initializing vision client: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set and points to a valid service account key file.")
