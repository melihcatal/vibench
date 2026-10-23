from typing import Any, Dict, List, Union


class HostedLLMRequest:
    def __init__(self, model_id: str, prompt: str, max_tokens: int):
        self.model_id = model_id
        self.prompt = prompt
        self.max_tokens = max_tokens


class HostedLLMResponse:
    def __init__(self, generated_text: str):
        self.generated_text = generated_text


def normalize_hosted_llm_response(response: HostedLLMResponse) -> str:
    return response.generated_text.strip()


class ModelFamilySelectionRequest:
    def __init__(self, model_family: str, criteria: Dict[str, Any]):
        self.model_family = model_family
        self.criteria = criteria


class ModelFamilySelectionResponse:
    def __init__(self, selected_model: str):
        self.selected_model = selected_model


def normalize_model_family_selection_response(response: ModelFamilySelectionResponse) -> str:
    return response.selected_model.strip()
