from google.cloud import vision
import os

def get_vision_client():
    """Returns an initialized Google Cloud Vision client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication.
    # Example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Please set it to the path of your service account key file for authentication.")
    
    return vision.ImageAnnotatorClient()

if __name__ == '__main__':
    # Example usage:
    # Set your GOOGLE_APPLICATION_CREDENTIALS environment variable before running
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    try:
        client = get_vision_client()
        print("Google Cloud Vision client initialized successfully.")
    except Exception as e:
        print(f"Error initializing client: {e}")
