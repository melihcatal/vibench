from google.cloud import vision
import os

def get_vision_client():
    """Provides a configured Google Cloud Vision client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    default authentication is configured.
    """
    # The client will automatically pick up credentials from the environment
    # (e.g., GOOGLE_APPLICATION_CREDENTIALS) or other default sources.
    return vision.ImageAnnotatorClient()

if __name__ == '__main__':
    print("Running vision_client.py example...")
    try:
        client = get_vision_client()
        print("Google Cloud Vision client created successfully.")
        # You can add a simple test call here if desired, e.g., to list features
        # However, making an actual API call would require an image and could incur costs.
    except Exception as e:
        print(f"Error creating Vision client: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS is set or you are authenticated.")
