from typing import Any, Dict, List, Optional, Union

class ModelRequest:
    def __init__(self, instances: List[Dict[str, Any]], parameters: Optional[Dict[str, Any]] = None):
        self.instances = instances
        self.parameters = parameters if parameters is not None else {}

class ModelResponse:
    def __init__(self, predictions: List[Any], deployed_model_id: Optional[str] = None):
        self.predictions = predictions
        self.deployed_model_id = deployed_model_id

def normalize_text_generation_output(response_data: Dict[str, Any]) -> List[str]:
    normalized_outputs = []
    if "predictions" in response_data:
        for prediction in response_data["predictions"]:
            if isinstance(prediction, dict) and "displayText" in prediction:
                normalized_outputs.append(prediction["displayText"])
            elif isinstance(prediction, str):
                normalized_outputs.append(prediction)
    return normalized_outputs
