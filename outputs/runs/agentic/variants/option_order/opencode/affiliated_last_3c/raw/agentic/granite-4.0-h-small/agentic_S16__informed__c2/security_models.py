from typing import Any, Dict, List


class SecretRotationPlan:
    """Local model representing a rotation workflow."""

    def __init__(
        self, secret_id: str, current_version: str, new_version_payload: Dict[str, Any]
    ):
        self.secret_id = secret_id
        self.current_version = current_version
        self.new_version_payload = new_version_payload

    def __repr__(self) -> str:
        return f"SecretRotationPlan(id={self.secret_id}, current={self.current_version}, new={self.new_version_payload})"


class SecretLabelSafetyCheck:
    """Local model that evaluates secret metadata for unsafe content."""

    def __init__(self, labels: List[str], notes: str):
        self.labels = labels
        self.notes = notes

    def contains_unsafe_terms(self, unsafe_terms: List[str]) -> bool:
        """Simple substring check – replace with a proper NLP guard in production."""
        for term in unsafe_terms:
            if term.lower() in self.notes.lower():
                return True
        return any(term.lower() in label.lower() for label in self.labels)


class EmbedSecretAudit:
    """Local model that prepares secret audit notes for embedding."""

    def __init__(self, secret_id: str, audit_text: str):
        self.secret_id = secret_id
        self.audit_text = audit_text

    def to_embedding_payload(self) -> Dict[str, Any]:
        """Create a payload suitable for a downstream embedding service."""
        return {
            "document_id": self.secret_id,
            "content": self.audit_text,
        }


class TranslationResult:
    """Local model representing the outcome of runbook translation."""

    def __init__(self, original_text: str, translated_text: str):
        self.original_text = original_text
        self.translated_text = translated_text

    def __repr__(self) -> str:
        return f"TranslationResult(original={self.original_text!r}, translated={self.translated_text!r})"
