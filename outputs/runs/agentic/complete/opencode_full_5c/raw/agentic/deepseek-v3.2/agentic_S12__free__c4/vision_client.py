import os
from typing import Dict, Any, Optional
import boto3
from google.cloud import vision
import requests


class VisionClient:
    """Local configuration and client helper utilities for Static Image and Visual Understanding."""

    @staticmethod
    def get_google_vision_client() -> vision.ImageAnnotatorClient:
        """Get Google Cloud Vision client."""
        return vision.ImageAnnotatorClient()

    @staticmethod
    def get_aws_rekognition_client():
        """Get AWS Rekognition client."""
        return boto3.client("rekognition")

    @staticmethod
    def get_openai_headers() -> Dict[str, str]:
        """Get headers for OpenAI API requests."""
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    @staticmethod
    def get_azure_vision_headers() -> Dict[str, str]:
        """Get headers for Azure Computer Vision API requests."""
        subscription_key = os.environ.get("AZURE_VISION_KEY")
        if not subscription_key:
            raise ValueError("AZURE_VISION_KEY environment variable is required")
        return {
            "Ocp-Apim-Subscription-Key": subscription_key,
            "Content-Type": "application/octet-stream",
        }

    @staticmethod
    def get_azure_vision_endpoint() -> str:
        """Get Azure Computer Vision endpoint."""
        endpoint = os.environ.get("AZURE_VISION_ENDPOINT")
        if not endpoint:
            raise ValueError("AZURE_VISION_ENDPOINT environment variable is required")
        return endpoint.rstrip("/")

    @staticmethod
    def read_image_as_bytes(image_path: str) -> bytes:
        """Read image file as bytes."""
        with open(image_path, "rb") as image_file:
            return image_file.read()

    @staticmethod
    def read_image_as_base64(image_path: str) -> str:
        """Read image file and encode as base64."""
        import base64

        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    @staticmethod
    def validate_image_path(image_path: str) -> bool:
        """Validate that image path exists and is readable."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        if not os.access(image_path, os.R_OK):
            raise PermissionError(f"Cannot read image file: {image_path}")
        return True
