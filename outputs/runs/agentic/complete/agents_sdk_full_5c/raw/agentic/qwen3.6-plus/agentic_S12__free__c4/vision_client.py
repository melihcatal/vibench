"""
Local configuration and client helper utilities for Static Image and Visual Understanding.
Uses Google Cloud Vision API (google-cloud-vision) as the concrete provider.
"""

import os
from typing import Optional

from google.cloud import vision_v1
from google.cloud.vision_v1 import ImageAnnotatorClient
from google.cloud.vision_v1.types import Image, AnnotateImageRequest, ImageContext
from google.api_core import client_options


def get_vision_client(
    credentials_path: Optional[str] = None,
    project_id: Optional[str] = None,
    api_endpoint: Optional[str] = None,
) -> ImageAnnotatorClient:
    """
    Initialize and return a Google Cloud Vision ImageAnnotatorClient.

    Args:
        credentials_path: Path to service account JSON file. Falls back to
                          GOOGLE_APPLICATION_CREDENTIALS env var.
        project_id: Google Cloud project ID. Falls back to GOOGLE_CLOUD_PROJECT env var.
        api_endpoint: Optional custom API endpoint.

    Returns:
        Configured ImageAnnotatorClient instance.
    """
    cred_path = credentials_path or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    proj_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "default-project")

    client_kwargs = {}

    if api_endpoint:
        client_kwargs["client_options"] = client_options.ClientOptions(
            api_endpoint=api_endpoint
        )

    if cred_path and os.path.exists(cred_path):
        from google.oauth2 import service_account

        credentials = service_account.Credentials.from_service_account_file(cred_path)
        client_kwargs["credentials"] = credentials
        client_kwargs["client_options"] = client_options.ClientOptions(
            api_endpoint=api_endpoint or "vision.googleapis.com"
        )

    client = ImageAnnotatorClient(**client_kwargs)
    return client


def load_image_from_path(image_path: str) -> Image:
    """
    Load a local image file into a Google Cloud Vision Image object.

    Args:
        image_path: Path to the image file on disk.

    Returns:
        Vision Image object with raw bytes content.
    """
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    return Image(content=content)


def load_image_from_url(image_uri: str) -> Image:
    """
    Create a Vision Image object from a public URI.

    Args:
        image_uri: Public HTTP/HTTPS or GCS URI (gs://...).

    Returns:
        Vision Image object with source URI.
    """
    source = vision_v1.ImageSource(image_uri=image_uri)
    return Image(source=source)


def build_annotate_request(
    image: Image,
    features: list,
    language_hints: Optional[list[str]] = None,
) -> AnnotateImageRequest:
    """
    Build an AnnotateImageRequest for the Vision API.

    Args:
        image: Vision Image object.
        features: List of Feature objects specifying detection types.
        language_hints: Optional BCP-47 language codes for text detection.

    Returns:
        Configured AnnotateImageRequest.
    """
    image_context = None
    if language_hints:
        image_context = ImageContext(language_hints=language_hints)

    return AnnotateImageRequest(
        image=image,
        features=features,
        image_context=image_context,
    )


def get_provider_info() -> dict:
    """
    Return provider identification metadata.

    Returns:
        Dictionary with provider details.
    """
    return {
        "provider": "google_cloud_vision",
        "service": "Google Cloud Vision API",
        "endpoint": "vision.googleapis.com",
        "client_class": "google.cloud.vision_v1.ImageAnnotatorClient",
    }
