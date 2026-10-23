class ModelRequest:
    def __init__(self, text: str, parameters: dict = None):
        self.text = text
        self.parameters = parameters or {}

    def to_bedrock_converse_format(self):
        return {"role": "user", "content": [{"text": self.text}]}

class ModelResponse:
    def __init__(self, raw_response: dict):
        self.raw_response = raw_response
        self.text = self._extract_text()
        self.metadata = self._extract_metadata()

    def _extract_text(self):
        if "output" in self.raw_response and "message" in self.raw_response["output"] and "content" in self.raw_response["output"]["message"]:
            return "".join(block["text"] for block in self.raw_response["output"]["message"]["content"] if "text" in block)
        return ""

    def _extract_metadata(self):
        metadata = {
            "usage": self.raw_response.get("usage"),
            "amazon_model_id": self.raw_response["output"]["responseMetadata"]["modelId"] if "output" in self.raw_response and "responseMetadata" in self.raw_response["output"] else None,
            "request_id": self.raw_response["output"]["responseMetadata"]["requestId"] if "output" in self.raw_response and "responseMetadata" in self.raw_response["output"] else None,
        }
        return metadata
