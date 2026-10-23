from typing import Dict, Any

class ModelClientConfig:
    def __init__(self, api_key: str, endpoint: str):
        self.api_key = api_key
        self.endpoint = endpoint

class ModelClient:
    def __init__(self, config: ModelClientConfig):
        self.config = config

    def invoke_model(self, model_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Placeholder for actual API call
        pass

    def get_model_metadata(self, model_id: str) -> Dict[str, Any]:
        # Placeholder for actual API call
        pass