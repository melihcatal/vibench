import json


class Normalizer:
    """Utility to standardize SDK responses into a consistent shape across providers.

    For Amazon Rekognition, maps label detection, text detection, and moderation labels
    to simple lists of strings.
    """

    @staticmethod
    def normalize_labels(response: dict) -> list:
        """Extract label names from Rekognition DetectLabels response."""
        return [label["Name"] for label in response.get("Labels", [])]

    @staticmethod
    def normalize_text(response: dict) -> list:
        """Extract detected text strings from DetectText response."""
        return [text["DetectedText"] for text in response.get("TextDetections", [])]

    @staticmethod
    def normalize_safety(response: dict) -> bool:
        """Interpret moderation result as a safety flag."""
        # Rekognition returns IsSafe = True/False in moderation labels
        return response.get("IsSafe", True)

    @staticmethod
    def normalize_description(response: dict) -> str:
        """Build a concise description from available fields."""
        # Priority: explicit description field, else assemble from labels
        if response.get("Description"):
            return response["Description"]
        labels = Normalizer.normalize_labels(response)
        if labels:
            return "Image contains " + ", ".join(labels)
        return "No recognizable content found."
