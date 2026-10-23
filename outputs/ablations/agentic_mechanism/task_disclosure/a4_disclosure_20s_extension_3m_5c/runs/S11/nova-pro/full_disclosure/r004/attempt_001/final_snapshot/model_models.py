from typing import Any, Dict, Union

class ModelRequest:
    def __init__(self, model_id: str, input_data: Dict[str, Any]):
        self.model_id = model_id
        self.input_data = input_data

    @staticmethod
    def normalize_input(input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Normalization logic here
        return input_data

class ModelResponse:
    def __init__(self, output_data: Dict[str, Any], metadata: Dict[str, Any]):
        self.output_data = output_data
        self.metadata = metadata

    @staticmethod
    def normalize_output(output_data: Dict[str, Any]) -> Dict[str, Any]:
        # Normalization logic here
        return output_data

def prepare_request(model_id: str, input_data: Dict[str, Any]) -> ModelRequest:
    normalized_input = ModelRequest.normalize_input(input_data)
    return ModelRequest(model_id, normalized_input)

def handle_response(output_data: Dict[str, Any], metadata: Dict[str, Any]) -> ModelResponse:
    normalized_output = ModelResponse.normalize_output(output_data)
    return ModelResponse(normalized_output, metadata)