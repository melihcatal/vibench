from typing import Dict, Any, Optional


class StreamingRecognitionConfig:
    """
    Local configuration model for streaming speech recognition.
    """

    def __init__(
        self,
        model: str,
        interim_results: bool = True,
        smart_formatting: bool = True,
        content_type: str = "audio/l16; rate=44100",
    ):
        self.model = model
        self.interim_results = interim_results
        self.smart_formatting = smart_formatting
        self.content_type = content_type


def normalize_response(response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Normalizes IBM Watson STT response into a consistent format.
    """
    if response.get("results"):
        result = response["results"][0]
        return {
            "text": result["alternatives"][0]["transcript"],
            "final": result.get("final", False),
            "confidence": result["alternatives"][0].get("confidence", 0.0),
        }
    return None
