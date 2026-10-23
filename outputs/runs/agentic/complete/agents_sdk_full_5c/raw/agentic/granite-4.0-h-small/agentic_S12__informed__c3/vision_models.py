# Utilities for normalizing Vision API request/response payloads

def prepare_image_bytes(image_bytes: bytes) -> Dict:
    """Wrap raw image bytes into a Google Vision request format."""
    from google.cloud.vision_v1.types import Image, ImageSource
    return {
        "image": Image(source=ImageSource(content=image_bytes)),
        "features": []  # Features will be populated by caller
    }


def extract_labels(response) -> List[str]:
    """Extract label annotations from Vision response."""
    return [annotation.description for annotation in response.label_annotations]


def extract_text(response) -> List[str]:
    """Extract OCR text from Vision response."""
    return [block.description for page in response.full_text_annotation.pages
            for line in page.blocks for block in line.blocks]


def extract_safe_search(response) -> Dict:
    """Extract safe‑search annotations."""
    return {
        "adult": response.safe_search_annotation.adult,
        "spoof": response.safe_search_annotation.spoof,
        "medical": response.safe_search_annotation.medical,
        "violence": response.safe_search_annotation.violence,
        "racy": response.safe_search_annotation.racy
    }
