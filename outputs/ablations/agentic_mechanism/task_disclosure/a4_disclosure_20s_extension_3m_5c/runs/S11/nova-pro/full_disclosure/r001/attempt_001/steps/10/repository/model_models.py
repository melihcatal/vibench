from typing import Any, Dict, Union

class ModelRequest:
    def __init__(self, model_id: str, input_data: Dict[str, Any]):
        self.model_id = model_id
        self.input_data = input_data

    def to_dict(self) -> Dict[str, Any]:
        return {
            'model_id': self.model_id,
            'input_data': self.input_data
        }

class ModelResponse:
    def __init__(self, output_data: Dict[str, Any], metadata: Dict[str, Any]):
        self.output_data = output_data
        self.metadata = metadata

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModelResponse':
        return cls(
            output_data=data.get('output_data', {}),
            metadata=data.get('metadata', {})
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'output_data': self.output_data,
            'metadata': self.metadata
        }

def normalize_output(response: ModelResponse) -> Dict[str, Any]:
    normalized_output = {}
    for key, value in response.output_data.items():
        if isinstance(value, Union[str, int, float]):
            normalized_output[key] = value
        elif isinstance(value, dict):
            normalized_output[key] = normalize_output(ModelResponse.from_dict(value))
    return normalized_output