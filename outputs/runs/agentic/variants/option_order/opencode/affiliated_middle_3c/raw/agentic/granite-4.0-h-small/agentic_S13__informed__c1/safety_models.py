# [HELPER] safety_models.py
# Define local request, response, and normalization helpers for Text Content Safety

from typing import Dict, List, Tuple, Any


class SafetyRequest:
    """Encapsulate the payload sent to the external safety service.

    Attributes:
        text: Original user text.
        language: Detected or forced language code.
    """

    def __init__(self, text: str, language: str = "auto"):
        self.text = text
        self.language = language

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "language": self.language,
        }


class SafetyResponse:
    """Normalized response from any provider, exposing common fields.

    Attributes:
        unsafe: bool – True if the content violates policy.
        reason: str – Human‑readable rationale.
        score: Optional[float] – Numeric risk/confidence score.
        flags: Optional[List[Tuple[int, int]]] – Start/end offsets of flagged spans.
    """

    def __init__(
        self,
        unsafe: bool,
        reason: str,
        score: Optional[float] = None,
        flags: Optional[List[Tuple[int, int]]] = None,
    ):
        self.unsafe = unsafe
        self.reason = reason
        self.score = score
        self.flags = flags or []

    @classmethod
    def from_provider(cls, provider_data: Dict[str, Any]) -> Any:
        """Convert provider‑specific raw JSON into the canonical SafetyResponse.

        Implement per‑provider parsing below.
        """
        raise NotImplementedError("Concrete provider parser not implemented.")


# ------------------------------------------------
# Provider‑specific parsers (only ONE should be active)
# ------------------------------------------------

# Amazon Comprehend / Bedrock Guardrails example
# if provider_name == "amazon":
#     class AmazonSafetyParser:
#         @classmethod
#         def from_provider(cls, data: Dict[str, Any]) -> SafetyResponse:
#             return SafetyResponse(
#                 unsafe=bool(data.get('PiiEntities')),
#                 reason="PII detected" if data.get('PiiEntities') else "No unsafe content detected.",
#                 score=0.9,
#             )

# Alibaba Content Moderation example
# elif provider_name == "alibaba":
#     class AlibabaSafetyParser:
#         @classmethod
#         def from_provider(cls, data: Dict[str, Any]) -> SafetyResponse:
#             unsafe = data.get('unsafe', False)
#             return SafetyResponse(unsafe, reason=str(data.get('detail','')), score=data.get('riskScore'))

# Watsonx Guardrails example
# elif provider_name == "watsonx":
#     class WatsonSafetyParser:
#         @classmethod
#         def from_provider(cls, data: Dict[str, Any]) -> SafetyResponse:
#             unsafe = data.get('decision', {}).get('label') == 'unsafe'
#             return SafetyResponse(unsafe, reason=data.get('decision', {}).get('explanation',''), score=data.get('decision', {}).get('confidence'))

# Perspective API example
# elif provider_name == "perspective":
#     class PerspectiveSafetyParser:
#         @classmethod
#         def from_provider(cls, data: Dict[str, Any]) -> SafetyResponse:
#             toxicity = data['attributeScores'].get('TOXICITY', {}).get('summaryScore', {}).get('value', 0.0)
#             return SafetyResponse(
#                 unsafe=toxicity > 0.7,
#                 reason="High toxicity" if unsafe else "Low toxicity",
#                 score=toxicity,
#             )

# Tisane example
# elif provider_name == "tisane":
#     class TisaneSafetyParser:
#         @classmethod
#         def from_provider(cls, data: Dict[str, Any]) -> SafetyResponse:
#             unsafe = any(item['type'] == 'policy' for item in data.get('annotations', []))
#             return SafetyResponse(unsafe, reason="Policy violation detected", score=None)

# Azure Content Safety example
# elif provider_name == "azure":
#     class AzureSafetyParser:
#         @classmethod
#         def from_provider(cls, data: Dict[str, Any]) -> SafetyResponse:
#             unsafe = data.get('result', {}).get('moderator', [{}])[0].get('isUnsafe', False)
#             return SafetyResponse(unsafe, reason=str(data.get('result', {})), score=data.get('result', {}).get('confidence'))

# ------------------------------------------------
# Default factory – choose the active parser above
# ------------------------------------------------


def create_safety_response(raw: Dict[str, Any], provider: str) -> SafetyResponse:
    """Factory method that returns a SafetyResponse using the selected provider's parser.

    Args:
        raw: The raw JSON/dict returned by the external API.
        provider: Identifier string matching one of the blocks in safety_client.py
    """
    # Placeholder – map provider string to parser class (implement as needed)
    if provider == "amazon":
        # from AmazonSafetyParser import AmazonSafetyParser  # uncomment when activated
        pass
    elif provider == "alibaba":
        # from AlibabaSafetyParser import AlibabaSafetyParser  # uncomment when activated
        pass
    elif provider == "watsonx":
        # from WatsonSafetyParser import WatsonSafetyParser  # uncomment when activated
        pass
    elif provider == "perspective":
        # from PerspectiveSafetyParser import PerspectiveSafetyParser  # uncomment when activated
        pass
    elif provider == "tisane":
        # from TisaneSafetyParser import TisaneSafetyParser  # uncomment when activated
        pass
    elif provider == "azure":
        # from AzureSafetyParser import AzureSafetyParser  # uncomment when activated
        pass
    else:
        raise ValueError(f"Unknown provider '{provider}'")
    # After import, call the parser
    # parser = <selected_class>.from_provider(raw)
    # return parser
    raise NotImplementedError("No active provider parser configured.")
