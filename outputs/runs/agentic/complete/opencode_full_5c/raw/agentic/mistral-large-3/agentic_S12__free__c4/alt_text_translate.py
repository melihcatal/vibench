from typing import Optional
from google.cloud import translate_v2 as translate
from vision_client import VisionClient
from vision_models import ImageDescription


class AltTextTranslator:
    """Translates generated image descriptions using Google Cloud Translation API."""

    def __init__(self):
        self.vision_client = VisionClient()
        self.translate_client = translate.Client()
        self.model = (
            "nmt"  # Google Cloud Translation's Neural Machine Translation model
        )

    def translate_description(
        self,
        image_path: Optional[str] = None,
        image_content: Optional[bytes] = None,
        target_language: str = "es",
    ) -> str:
        """Translates an image description to the target language.

        Args:
            image_path: Local path to the image file.
            image_content: Raw image bytes.
            target_language: Target language code (e.g., 'es', 'fr', 'de').

        Returns:
            Translated image description.
        """
        # Generate description using Vision API
        image = self.vision_client.load_image(image_path, image_content)
        feature_types = [
            vision_v1.Feature.Type.LABEL_DETECTION,
            vision_v1.Feature.Type.IMAGE_PROPERTIES,
        ]
        results = self.vision_client.detect_features(image, feature_types)

        description = self._generate_description(results)

        # Translate description
        translation = self.translate_client.translate(
            description, target_language=target_language, model=self.model
        )

        return translation["translatedText"]

    def _generate_description(self, results: Dict[str, Any]) -> str:
        """Generates a description from Vision API results."""
        description_parts = []

        if results.get("labels"):
            labels = [label.description for label in results["labels"]]
            description_parts.append(f"Image likely contains: {', '.join(labels[:3])}.")

        if results.get("colors"):
            description_parts.append(
                f"Dominant colors: {', '.join(results['colors'][:3])}."
            )

        return (
            " ".join(description_parts)
            if description_parts
            else "No description available."
        )
