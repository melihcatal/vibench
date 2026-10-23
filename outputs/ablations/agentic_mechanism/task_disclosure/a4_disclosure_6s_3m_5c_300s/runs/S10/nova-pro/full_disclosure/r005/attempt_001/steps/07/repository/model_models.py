from typing import Any, Dict, List, Union

class LLMRequest:
    def __init__(self, model_family: str, prompt: str, parameters: Dict[str, Any]):
        self.model_family = model_family
        self.prompt = prompt
        self.parameters = parameters

    def to_dict(self) -> Dict[str, Any]:
        return {
            'model_family': self.model_family,
            'prompt': self.prompt,
            'parameters': self.parameters
        }


class LLMResponse:
    def __init__(self, output: str, metadata: Dict[str, Any]):
        self.output = output
        self.metadata = metadata

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LLMResponse':
        return cls(
            output=data['output'],
            metadata=data['metadata']
        )


def normalize_response(response: Union[str, Dict[str, Any]]) -> LLMResponse:
    if isinstance(response, str):
        return LLMResponse(output=response, metadata={})
    elif isinstance(response, dict):
        return LLMResponse.from_dict(response)
    else:
        raise ValueError('Invalid response format')


MODEL_FAMILIES = {
    'amazon-nova-api/nova-pro-v1': 'Amazon Nova Pro V1',
    'google-palm-api/palm-v2': 'Google Palm V2',
    'openai-api/gpt-4': 'OpenAI GPT-4'
}