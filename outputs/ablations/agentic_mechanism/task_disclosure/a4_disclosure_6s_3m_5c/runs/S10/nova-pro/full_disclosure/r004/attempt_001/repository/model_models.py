from typing import Any, Dict, List, Union

class ModelRequest:
    def __init__(self, model_id: str, prompt: str, parameters: Dict[str, Any]):
        self.model_id = model_id
        self.prompt = prompt
        self.parameters = parameters

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ModelRequest':
        return ModelRequest(
            model_id=data['model_id'],
            prompt=data['prompt'],
            parameters=data['parameters']
        )

class ModelResponse:
    def __init__(self, model_id: str, output: Union[str, List[str]]):
        self.model_id = model_id
        self.output = output

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ModelResponse':
        return ModelResponse(
            model_id=data['model_id'],
            output=data['output']
        )

def normalize_response(response: Dict[str, Any]) -> ModelResponse:
    if 'choices' in response:
        output = [choice['text'] for choice in response['choices']]
    else:
        output = response['output']
    return ModelResponse(
        model_id=response['model_id'],
        output=output
    )