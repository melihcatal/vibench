from typing import Dict, Any, List, Optional
import json


class PlatformModelRequest:
    def __init__(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_output_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        **kwargs,
    ):
        self.prompt = prompt
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.top_p = top_p
        self.top_k = top_k
        self.extra_params = kwargs

    def to_dict(self) -> Dict[str, Any]:
        request_dict = {"prompt": self.prompt}
        if self.temperature is not None:
            request_dict["temperature"] = self.temperature
        if self.max_output_tokens is not None:
            request_dict["max_output_tokens"] = self.max_output_tokens
        if self.top_p is not None:
            request_dict["top_p"] = self.top_p
        if self.top_k is not None:
            request_dict["top_k"] = self.top_k
        request_dict.update(self.extra_params)
        return request_dict


class PlatformModelResponse:
    def __init__(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
        raw_response: Any = None,
    ):
        self.text = text
        self.metadata = metadata if metadata is not None else {}
        self.raw_response = raw_response

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "metadata": self.metadata,
            "raw_response": str(
                self.raw_response
            ),  # Convert raw_response to string for serialization
        }

    @classmethod
    def from_vertex_ai_response(cls, response):
        text = response.text
        metadata = {
            "model_name": "gemini-pro",  # Placeholder, actual model name could be passed from client
            "prompt_tokens": response.usage_metadata.prompt_token_count
            if response.usage_metadata
            else None,
            "candidates_tokens": response.usage_metadata.candidates_token_count
            if response.usage_metadata
            else None,
            "total_tokens": response.usage_metadata.total_token_count
            if response.usage_metadata
            else None,
            "finish_reason": response.candidates[0].finish_reason.name
            if response.candidates
            else None,
        }
        return cls(text=text, metadata=metadata, raw_response=response)


if __name__ == "__main__":
    # Example Usage
    req = PlatformModelRequest(prompt="Generate a short poem.", temperature=0.7)
    print("Request dict:", req.to_dict())

    # Mock Vertex AI response for demonstration
    class MockUsageMetadata:
        prompt_token_count = 10
        candidates_token_count = 20
        total_token_count = 30

    class MockCandidate:
        class MockFinishReason:
            name = "STOP"

        finish_reason = MockFinishReason()

    class MockVertexAIResponse:
        text = "A gentle breeze, a sky so blue,\nNature's beauty, fresh and new."
        usage_metadata = MockUsageMetadata()
        candidates = [MockCandidate()]

    mock_vertex_ai_response = MockVertexAIResponse()
    res = PlatformModelResponse.from_vertex_ai_response(mock_vertex_ai_response)
    print("Response dict:", json.dumps(res.to_dict(), indent=2))
