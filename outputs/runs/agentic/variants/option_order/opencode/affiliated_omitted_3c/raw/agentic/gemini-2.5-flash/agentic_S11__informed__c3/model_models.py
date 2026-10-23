from typing import Dict, Any


class ModelRequest:
    def __init__(self, prompt: str, model_name: str = "qwen-turbo", **kwargs):
        self.prompt = prompt
        self.model_name = model_name
        self.extra_params = kwargs

    def to_dashscope_payload(self) -> Dict[str, Any]:
        payload = {
            "model": self.model_name,
            "prompt": self.prompt,
        }
        payload.update(self.extra_params)
        return payload


class ModelResponse:
    def __init__(self, raw_response: Any):
        self.raw_response = raw_response
        self.text_output = self._extract_text_output()
        self.metadata = self._extract_metadata()

    def _extract_text_output(self) -> str:
        if (
            self.raw_response
            and self.raw_response.output
            and self.raw_response.output.text
        ):
            return self.raw_response.output.text
        return ""

    def _extract_metadata(self) -> Dict[str, Any]:
        metadata = {}
        if self.raw_response:
            metadata["request_id"] = self.raw_response.request_id
            if self.raw_response.usage:
                metadata["usage"] = self.raw_response.usage.to_dict()
        return metadata
