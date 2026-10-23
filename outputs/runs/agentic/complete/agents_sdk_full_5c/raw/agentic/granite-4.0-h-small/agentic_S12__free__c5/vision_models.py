import os

def get_image_path(image_uri):
    """Resolve an image URI (local path, GCS path, or public HTTP URL) to a local file path used by the SDK."""
    if image_uri.startswith(('http://', 'https://')):
        # Download temporarily to a cache location (placeholder implementation)
        import tempfile, urllib.request
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            urllib.request.urlretrieve(image_uri, tmp.name)
            return tmp.name
    # Assume local path or GCS path (GCS handled by SDK via gs://)
    return image_uri

# Mapping of concepts to Vision SDK model IDs (placeholder)
MODEL_IDS = {
    'label_detection': 'GOOGLE_VISION_LABEL',
    'document_text_detection': 'GOOGLE_VISION_OCR',
    'text_detection': 'GOOGLE_VISION_TEXT',
    'safe_search_detection': 'GOOGLE_VISION_SAFE',
}

def model_for_task(task_name):
    """Return the provider model identifier for a given visual analysis task."""
    return MODEL_IDS.get(task_name, 'UNKNOWN')
