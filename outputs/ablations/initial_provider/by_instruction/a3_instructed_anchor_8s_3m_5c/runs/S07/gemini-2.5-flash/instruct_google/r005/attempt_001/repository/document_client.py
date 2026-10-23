import os

class DocumentClient:
    """Provides a base for document processing client configurations."""
    def __init__(self):
        # This client can be extended to manage different provider clients
        # or common authentication.
        pass

    def get_google_vision_client(self):
        from google.cloud import vision
        return vision.ImageAnnotatorClient()

