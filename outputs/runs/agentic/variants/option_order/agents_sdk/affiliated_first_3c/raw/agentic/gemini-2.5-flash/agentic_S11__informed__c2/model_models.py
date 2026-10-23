from typing import Dict, Any, Optional

class PromptRequest:
    def __init__(self, text_input: str, model_config: Optional[Dict[str, Any]] = None):
        self.text_input = text_input
        self.model_config = model_config if model_config is not None else {}

    def to_provider_format(self) -> str:
        # For Vertex AI, a simple string is often enough for text prompts
        return self.text_input

class ModelResponse:
    def __init__(self, raw_response: Any):
        self._raw_response = raw_response

    @property
    def generated_text(self) -> str:
        # Assuming raw_response is a vertexai.generative_models.GenerateContentResponse
        return self._raw_response.text if hasattr(self._raw_response, 'text') else str(self._raw_response)

    @property
    def metadata(self) -> Dict[str, Any]:
        meta = {}
        if hasattr(self._raw_response, 'usage_metadata') and self._raw_response.usage_metadata:
            meta["prompt_token_count"] = self._raw_response.usage_metadata.prompt_token_count
            meta["candidates_token_count"] = self._raw_response.usage_metadata.candidates_token_count
            meta["total_token_count"] = self._raw_response.usage_metadata.total_token_count
        # Add other relevant metadata from the raw response object
        return meta

    def get_raw_response(self) -> Any:
        return self._raw_response

if __name__ == '__main__':
    # Example of usage:
    # from vertexai.generative_models import GenerateContentResponse
    # # This would normally come from a model invocation
    # mock_raw_response = type('MockResponse', (object,), {'text': 'Mocked text', 'usage_metadata': type('MockUsageMetadata', (object,), {'prompt_token_count': 10, 'total_token_count': 20})})()
    # response = ModelResponse(mock_raw_response)
    # print(response.generated_text)
    # print(response.metadata)
    pass
