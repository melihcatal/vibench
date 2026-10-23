from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ModerationRequest:
    text: str

@dataclass
class ModerationResponse:
    toxicity: float = 0.0
    sexual_content: float = 0.0
    violence: float = 0.0
    hate_speech: float = 0.0
    harassment: float = 0.0
    self_harm: float = 0.0
    profanity: float = 0.0

@dataclass
class RedactionRequest:
    text: str

@dataclass
class RedactionResponse:
    redacted_text: str

def normalize_azure_content_safety_response(azure_response) -> ModerationResponse:
    response = ModerationResponse()
    for category in azure_response.categories_analysis:
        # Azure Content Safety categories include Hate, SelfHarm, Sexual, Violence
        # Mapping to a generic ModerationResponse structure
        if category.category == "Hate":
            response.hate_speech = category.severity / 7
        elif category.category == "SelfHarm":
            response.self_harm = category.severity / 7
        elif category.category == "Sexual":
            response.sexual_content = category.severity / 7
        elif category.category == "Violence":
            response.violence = category.severity / 7
        # Toxicity and Profanity are not directly mapped in Azure CS categories, using a placeholder/max for now
        # In a real scenario, custom classification or other models would be used for these.
        # For now, let's assume toxicity is a general measure based on max severity.
        response.toxicity = max(response.toxicity, category.severity / 7)

    return response
