import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from typing import Optional


class ImageDescriber:
    """Generates a short visual description for an image using Google Cloud Vision API."""

    def __init__(self):
        self.client = vision_v1.ImageAnnotatorClient()
        self.model = (
            "builtin/stable"  # Google Cloud Vision's default image properties model
        )

    def describe(
        self, image_path: Optional[str] = None, image_content: Optional[bytes] = None
    ) -> str:
        """Generates a short visual description for an image.

        Args:
            image_path: Local path to the image file.
            image_content: Raw image bytes.

        Returns:
            A short visual description of the image.
        """
        if image_path:
            with open(image_path, "rb") as image_file:
                content = image_file.read()
        elif image_content:
            content = image_content
        else:
            raise ValueError("Either image_path or image_content must be provided.")

        image = types.Image(content=content)
        response = self.client.image_properties(image=image)

        # Extract dominant colors
        colors = response.image_properties_annotation.dominant_colors.colors
        color_descriptions = [
            f"{color.color.red}, {color.color.green}, {color.color.blue}"
            for color in colors
        ]

        # Generate a basic description
        description = f"Image with dominant colors: {', '.join(color_descriptions)}."

        # Use label detection to enrich description
        label_response = self.client.label_detection(image=image)
        labels = [label.description for label in label_response.label_annotations[:3]]
        if labels:
            description += f" Likely contains: {', '.join(labels)}."

        return description
