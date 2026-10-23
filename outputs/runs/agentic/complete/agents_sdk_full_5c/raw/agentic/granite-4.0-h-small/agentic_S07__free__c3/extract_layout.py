import os
import requests
from document_models import OCRResponse

def check_layout_quality(layout: dict) -> bool:
    """Evaluate layout extraction confidence using GCP Document AI confidence fields.
    """
    endpoint = os.getenv("GCP_DOCUMENTAI_ENDPOINT")
    if not endpoint:
        raise RuntimeError("GCP Document AI endpoint not configured")
    # Placeholder: normally you would POST the image and inspect 'confidence' fields.
    # Here we simulate a check: if bounding boxes are missing, flag low quality.
    if not layout.get('blocks'):
        return False
    return True

# Example usage (not executed here)
# if not check_layout_quality(layout_response):
#     # trigger fallback extraction method
