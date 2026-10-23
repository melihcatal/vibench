from typing import Dict, Any

class PlatformModelRequest:
    def __init__(self, text: str, parameters: Dict[str, Any] = None):
        self.text = text
        self.parameters = parameters if parameters is not None else {}

    def to_bedrock_converse_format(self):
        # A basic conversion for the text-only use case demonstrated
        return {"messages": [{"role": "user", "content": [{"text": self.text}]}]}

class PlatformModelResponse:
    def __init__(self, text: str, metadata: Dict[str, Any] = None, raw_response: Dict[str, Any] = None):
        self.text = text
        self.metadata = metadata if metadata is not None else {}
        self.raw_response = raw_response if raw_response is not None else {}

    @classmethod
    def from_bedrock_converse_response(cls, response: Dict[str, Any]):
        text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
        metadata = {"usage": response.get("usage"), "model_id": response["output"]["message"]["modelId"]}
        return cls(text=text, metadata=metadata, raw_response=response)
