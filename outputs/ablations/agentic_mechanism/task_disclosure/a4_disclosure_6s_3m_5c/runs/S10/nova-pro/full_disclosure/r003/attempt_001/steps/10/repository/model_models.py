from typing import Any, Dict, List, Union

class ModelRequest:
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


class ModelResponse:
    def __init__(self, model_family: str, output: Union[str, List[str]], metadata: Dict[str, Any]):
        self.model_family = model_family
        self.output = output
        self.metadata = metadata

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            model_family=data['model_family'],
            output=data['output'],
            metadata=data['metadata']
        )


def normalize_response(response: ModelResponse) -> Dict[str, Any]:
    normalized_response = {
        'model_family': response.model_family,
        'output': response.output,
        'metadata': response.metadata
    }
    return normalized_response
