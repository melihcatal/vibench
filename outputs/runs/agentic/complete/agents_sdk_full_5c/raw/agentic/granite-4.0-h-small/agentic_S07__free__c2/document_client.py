import os

class LayoutClient:
    """Helper for invoking the Layout Extraction provider API (Google Document AI)."""
    def __init__(self):
        # Set GOOGLE_APPLICATION_CREDENTIALS env var elsewhere if needed
        pass
    def process_document(self, image_path: str) -> dict:
        # Placeholder for actual API call
        return {'pages': [{'layout': []}]}
    def extract_tables(self, image_path: str) -> dict:
        # Placeholder for actual API call
        return {'cells': [], 'rows': []}
