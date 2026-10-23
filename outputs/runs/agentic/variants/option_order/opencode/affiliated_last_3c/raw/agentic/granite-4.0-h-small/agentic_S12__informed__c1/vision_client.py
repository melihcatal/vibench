import os
import dashscope
from typing import Optional


class VisionClient:
    """Local helper providing a unified SDK interface to DashScope multimodal vision API.
    All method signatures accept local file paths or buffers.
    """

    def __init__(self):
        # Environment variable holding the DashScope API key
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            raise RuntimeError("Missing DASHSCOPE_API_KEY environment variable")
        # DashScope SDK does not require further configuration for image APIs
        self._client = dashscope.Multimodal(self._credentials(api_key))

    @staticmethod
    def _credentials(api_key: str):
        return {"api_key": api_key}

    def labels(self, request: "LabelsRequest") -> "LabelsResponse":
        return self._client.labels(**request.to_dict())

    def description(self, request: "DescriptionRequest") -> "DescriptionResponse":
        return self._client.description(**request.to_dict())

    def text_detection(
        self, request: "TextDetectionRequest"
    ) -> "TextDetectionResponse":
        return self._client.text_detection(**request.to_dict())

    def safety_check(self, request: "SafetyCheckRequest") -> "SafetyCheckResponse":
        return self._client.safety_check(**request.to_dict())
