from typing import Dict, Any

class PlatformInvocationRequest:
    def __init__(self, text: str, model_id: str = "us.amazon.nova-pro-v1:0"):
        self.text = text
        self.model_id = model_id

    def to_bedrock_converse_payload(self) -> Dict[str, Any]:
        return {
            "modelId": self.model_id,
            "messages": [{"role": "user", "content": [{"text": self.text}]}],
        }

class PlatformInvocationResponse:
    def __init__(self, response_data: Dict[str, Any]):
        self._response_data = response_data
        self.text = self._extract_text(response_data)
        self.metadata = self._extract_metadata(response_data)

    def _extract_text(self, response_data: Dict[str, Any]) -> str:
        return "".join(block["text"] for block in response_data["output"]["message"]["content"] if "text" in block)

    def _extract_metadata(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "usage": response_data.get("usage"),
            "stop_reason": response_data.get("stopReason"),
            "model_id": response_data.get("modelId"),
        }

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "metadata": self.metadata, "_original_response": self._response_data}
