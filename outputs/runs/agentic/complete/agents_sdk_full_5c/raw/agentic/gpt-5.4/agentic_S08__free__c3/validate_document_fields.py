from __future__ import annotations

from typing import Any, Dict, List

from google.cloud import language_v2

from document_models import ValidationResult

GOOGLE_LANGUAGE_MODEL = "google-cloud-language-v2"


class DocumentFieldValidator:
    def __init__(self, language_client: language_v2.LanguageServiceClient | None = None):
        self.language_client = language_client or language_v2.LanguageServiceClient()

    def validate(self, extracted: Dict[str, Any], min_confidence: float = 0.5) -> Dict[str, Any]:
        errors: List[str] = []
        warnings: List[str] = []
        confidences: Dict[str, float] = {}

        doc_type = extracted.get("document_type")
        if doc_type == "invoice":
            required = ["vendor", "invoice_date", "total"]
        elif doc_type == "receipt":
            required = ["merchant", "total"]
        else:
            required = ["total"]

        for field_name in required:
            value = extracted.get(field_name)
            if value in (None, "", []):
                errors.append(f"Missing required field: {field_name}")

        notes = extracted.get("notes") or ""
        if notes:
            document = language_v2.Document(content=notes, type_=language_v2.Document.Type.PLAIN_TEXT)
            response = self.language_client.analyze_sentiment(request={"document": document})
            sentiment_score = float(response.document_sentiment.score)
            confidences["notes_sentiment_score"] = abs(sentiment_score)
            if sentiment_score < -0.8:
                warnings.append("Notes contain strongly negative language and may need review")

        raw_fields = extracted.get("raw_fields", {})
        for field_name, field_payload in raw_fields.items():
            confidence = field_payload.get("confidence")
            if confidence is not None:
                confidences[field_name] = float(confidence)
                if float(confidence) < min_confidence:
                    warnings.append(f"Low confidence for field: {field_name}")

        result = ValidationResult(valid=not errors, errors=errors, warnings=warnings, field_confidences=confidences)
        return {
            "valid": result.valid,
            "errors": result.errors,
            "warnings": result.warnings,
            "field_confidences": result.field_confidences,
            "provider": GOOGLE_LANGUAGE_MODEL,
        }
