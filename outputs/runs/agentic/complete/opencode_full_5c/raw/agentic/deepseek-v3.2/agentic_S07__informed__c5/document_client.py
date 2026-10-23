import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def get_document_client() -> DocumentIntelligenceClient:
    """Create and return an Azure Document Intelligence client."""
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Please set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY environment variables"
        )

    credential = AzureKeyCredential(key)
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=credential)
    return client


def validate_image_file(image_path: str) -> bool:
    """Validate that the image file exists and is readable."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    if not os.path.isfile(image_path):
        raise ValueError(f"Path is not a file: {image_path}")

    try:
        with open(image_path, "rb") as f:
            f.read(1024)
        return True
    except IOError as e:
        raise ValueError(f"Cannot read image file: {e}")


def get_supported_formats() -> list[str]:
    """Return list of supported image formats."""
    return [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".pdf"]


def format_bounding_box(bbox) -> str:
    """Format bounding box coordinates for display."""
    if not bbox:
        return "N/A"
    return f"({bbox.x:.1f}, {bbox.y:.1f}, {bbox.width:.1f}, {bbox.height:.1f})"
