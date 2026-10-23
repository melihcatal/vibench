from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class ContentSafetyResponse:
    """Defines a normalized response structure for Text Content Safety results (e.g., from Azure AI Content Safety)."""
    hate_severity: int = 0
    self_harm_severity: int = 0
    sexual_severity: int = 0
    violence_severity: int = 0
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_azure_response(cls, api_response: Dict[str, Any]) -> "ContentSafetyResponse":
        """Normalizes a raw Azure AI Content Safety API response into ContentSafetyResponse."""
        hate_severity = 0
        self_harm_severity = 0
        sexual_severity = 0
        violence_severity = 0

        for category_analysis in api_response.get("categoriesAnalysis", []):
            category = category_analysis.get("category")
            severity = category_analysis.get("severity", 0)
            if category == "Hate":
                hate_severity = severity
            elif category == "SelfHarm":
                self_harm_severity = severity
            elif category == "Sexual":
                sexual_severity = severity
            elif category == "Violence":
                violence_severity = severity
        
        return cls(
            hate_severity=hate_severity,
            self_harm_severity=self_harm_severity,
            sexual_severity=sexual_severity,
            violence_severity=violence_severity
        )


@dataclass
class ContentSafetyRequest:
    """Defines a normalized request structure for Text Content Safety."""
    text: str
    categories: Optional[list[str]] = None
    # Add other common request parameters if needed across providers

    def to_azure_payload(self) -> Dict[str, Any]:
        """Converts the normalized request to an Azure AI Content Safety specific payload."""
        payload = {"text": self.text}
        if self.categories:
            payload["categories"] = self.categories
        else:
            # Default categories for Azure if not specified
            payload["categories"] = ["Hate", "SelfHarm", "Sexual", "Violence"]
        payload["outputType"] = "FourSeverityLevels"
        return payload
