import os

# ---------------------------------------------------------------------------
# Helper: Configuration for Static Image and Visual Understanding
# ---------------------------------------------------------------------------


class VisionClient:
    """
    Central wrapper that initializes the concrete provider (Azure AI Vision in this example)
    and exposes simple methods used by the scenario files.
    """

    def __init__(self):
        # Provider credentials are expected as environment variables
        self.endpoint = os.getenv("AZURE_VISION_ENDPOINT")
        self.key = os.getenv("AZURE_VISION_KEY")
        if not self.endpoint or not self.key:
            raise RuntimeError(
                "Set AZURE_VISION_ENDPOINT and AZURE_VISION_KEY environment variables"
            )
        # Import the Azure SDK client lazily (only when code runs)
        from azure.ai.vision import VisionClient as AzureVisionClient

        # Instantiate the Azure client
        self._sdk_client = AzureVisionClient(
            endpoint=self.endpoint, credential=self.key
        )

    # -----------------------------------------------------------------------
    # Label detection (objects/labels)
    # -----------------------------------------------------------------------
    def label_image(self, image_path: str):
        """Azure AI Vision label detection"""
        with open(image_path, "rb") as img:
            result = self._sdk_client.analyze_image(img, features=["Labels"])
        # The SDK returns a list of Label objects; return them directly
        return result.labels

    # -----------------------------------------------------------------------
    # Image description (short caption)
    # -----------------------------------------------------------------------
    def describe_image(self, image_path: str) -> str:
        """Azure AI Vision generate short description"""
        with open(image_path, "rb") as img:
            result = self._sdk_client.analyze_image(img, features=["Description"])
        # Return the first generated caption (if any)
        return (
            result.description.captions[0].text if result.description.captions else ""
        )

    # -----------------------------------------------------------------------
    # OCR (text detection)
    # -----------------------------------------------------------------------
    def ocr_image(self, image_path: str):
        """Azure AI Vision OCR"""
        with open(image_path, "rb") as img:
            result = self._sdk_client.analyze_image(img, features=["Ocr"])
        # Each OCR result contains lines; each line contains words
        return result.ocr.result.lines

    # -----------------------------------------------------------------------
    # Safety / policy check
    # -----------------------------------------------------------------------
    def safe_content_check(self, image_path: str) -> bool:
        """Azure AI Content Safety – visual content policy check"""
        # In this example we reuse the same endpoint/key for demo purposes.
        # A real deployment would use the dedicated Content Safety service.
        with open(image_path, "rb") as img:
            # Simple HTTP request placeholder – replace with actual SDK call
            # safe = self._content_safety_client.check_content(img)
            safe = True  # placeholder – assume safe for demo
        return safe
