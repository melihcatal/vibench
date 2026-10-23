import os
import json
from typing import Dict, Any, List, Optional
import boto3


class ComplianceNoteTranslator:
    def __init__(self):
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

        self.translate_client = None
        self._initialize_client()

    def _initialize_client(self):
        if self.aws_access_key_id and self.aws_secret_access_key:
            self.translate_client = boto3.client(
                "translate",
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.aws_region,
            )
        else:
            self.translate_client = boto3.client(
                "translate", region_name=self.aws_region
            )

    def translate_compliance_note(
        self, text: str, target_language: str, source_language: str = "auto"
    ) -> Dict[str, Any]:
        """
        Translate encryption or compliance notes for reviewers.

        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'es', 'fr', 'de')
            source_language: Source language code or 'auto' for auto-detection

        Returns:
            Translation result with metadata
        """
        try:
            response = self.translate_client.translate_text(
                Text=text,
                SourceLanguageCode=source_language,
                TargetLanguageCode=target_language,
            )

            return {
                "translated_text": response["TranslatedText"],
                "source_language": response["SourceLanguageCode"],
                "target_language": response["TargetLanguageCode"],
                "original_text": text,
                "applied_terminology": response.get("AppliedTerminologies", []),
            }

        except self.translate_client.exceptions.InvalidRequestException as e:
            raise ValueError(f"Invalid translation request: {str(e)}") from e
        except self.translate_client.exceptions.TextSizeLimitExceededException as e:
            raise ValueError(f"Text too large for translation") from e
        except Exception as e:
            raise RuntimeError(f"Translation failed: {str(e)}") from e

    def translate_audit_trail(
        self,
        audit_notes: List[str],
        target_language: str,
        source_language: str = "auto",
    ) -> List[Dict[str, Any]]:
        """
        Translate multiple audit trail notes.

        Args:
            audit_notes: List of audit notes to translate
            target_language: Target language code
            source_language: Source language code or 'auto'

        Returns:
            List of translation results
        """
        results = []
        for note in audit_notes:
            try:
                result = self.translate_compliance_note(
                    note, target_language, source_language
                )
                results.append(result)
            except Exception as e:
                results.append(
                    {"error": str(e), "original_text": note, "translated_text": None}
                )

        return results

    def translate_crypto_terms(
        self, terms: Dict[str, str], target_language: str
    ) -> Dict[str, Any]:
        """
        Translate cryptographic terminology.

        Args:
            terms: Dictionary of terms to translate
            target_language: Target language code

        Returns:
            Translated terms with context
        """
        translated_terms = {}
        failed_terms = []

        for term, description in terms.items():
            try:
                term_result = self.translate_compliance_note(term, target_language)
                desc_result = self.translate_compliance_note(
                    description, target_language
                )

                translated_terms[term] = {
                    "term_translation": term_result["translated_text"],
                    "description_translation": desc_result["translated_text"],
                    "original_term": term,
                    "original_description": description,
                }
            except Exception as e:
                failed_terms.append({"term": term, "error": str(e)})

        return {
            "translated_terms": translated_terms,
            "failed_terms": failed_terms,
            "total_terms": len(terms),
            "successful_translations": len(translated_terms),
        }

    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect language of compliance note.

        Args:
            text: Text to analyze

        Returns:
            Language detection results
        """
        try:
            response = self.translate_client.translate_text(
                Text=text[:100],  # Sample for detection
                SourceLanguageCode="auto",
                TargetLanguageCode="en",  # Default target
            )

            return {
                "detected_language": response["SourceLanguageCode"],
                "confidence": "high",  # Amazon Translate returns high confidence detections
                "sample_text": text[:100],
                "full_text_length": len(text),
            }

        except Exception as e:
            raise RuntimeError(f"Language detection failed: {str(e)}") from e

    def create_multilingual_summary(
        self, compliance_data: Dict[str, Any], target_languages: List[str]
    ) -> Dict[str, Any]:
        """
        Create multilingual summary of compliance data.

        Args:
            compliance_data: Compliance data to summarize and translate
            target_languages: List of target language codes

        Returns:
            Multilingual summaries
        """
        summary_text = self._create_compliance_summary(compliance_data)

        translations = {}
        for lang in target_languages:
            try:
                translation = self.translate_compliance_note(summary_text, lang)
                translations[lang] = translation
            except Exception as e:
                translations[lang] = {
                    "error": str(e),
                    "language": lang,
                    "translated_text": None,
                }

        return {
            "original_summary": summary_text,
            "translations": translations,
            "source_language": "en",
            "target_languages": target_languages,
        }

    def _create_compliance_summary(self, compliance_data: Dict[str, Any]) -> str:
        """Create summary text from compliance data."""
        parts = []

        if "audit_findings" in compliance_data:
            findings = compliance_data["audit_findings"]
            parts.append(f"Audit Findings: {len(findings)} issues identified")

        if "key_management" in compliance_data:
            km = compliance_data["key_management"]
            parts.append(
                f"Key Management: {km.get('total_keys', 0)} keys, {km.get('rotated_keys', 0)} rotated"
            )

        if "encryption_operations" in compliance_data:
            ops = compliance_data["encryption_operations"]
            parts.append(f"Encryption Operations: {ops.get('total', 0)} operations")

        if "compliance_status" in compliance_data:
            status = compliance_data["compliance_status"]
            parts.append(f"Compliance Status: {status}")

        if "recommendations" in compliance_data:
            recs = compliance_data["recommendations"]
            parts.append(f"Recommendations: {len(recs)} items")

        return ". ".join(parts)


def translate_for_reviewers(text: str, target_language: str = "es") -> str:
    """
    Convenience function to translate compliance notes.

    Args:
        text: Text to translate
        target_language: Target language code

    Returns:
        Translated text
    """
    translator = ComplianceNoteTranslator()
    result = translator.translate_compliance_note(text, target_language)
    return result["translated_text"]
