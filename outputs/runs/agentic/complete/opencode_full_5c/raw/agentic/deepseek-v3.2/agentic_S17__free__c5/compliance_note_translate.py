import os
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import boto3
from botocore.exceptions import ClientError


@dataclass
class ComplianceNote:
    """Model for compliance notes."""

    note_id: str
    content: str
    language: str = "en"
    category: str = "encryption"
    severity: str = "medium"
    regulation: Optional[str] = None
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class TranslatedNote:
    """Model for translated compliance notes."""

    original_note: ComplianceNote
    translated_content: str
    target_language: str
    translation_confidence: float
    provider: str = "aws_translate"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "original_note": self.original_note.to_dict(),
            "translated_content": self.translated_content,
            "target_language": self.target_language,
            "translation_confidence": self.translation_confidence,
            "provider": self.provider,
        }


class ComplianceNoteTranslator:
    """Translate encryption or compliance notes for reviewers using AWS Translate."""

    def __init__(self, region: Optional[str] = None):
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self.translate = boto3.client("translate", region_name=self.region)

        # Supported languages for compliance translations
        self.supported_languages = [
            "en",
            "es",
            "fr",
            "de",
            "it",
            "pt",
            "ja",
            "ko",
            "zh",
            "ar",
        ]

        # Compliance terminology glossary (could be expanded)
        self.compliance_glossary = {
            "encryption": {
                "en": "encryption",
                "es": "cifrado",
                "fr": "chiffrement",
                "de": "Verschlüsselung",
                "it": "crittografia",
                "pt": "criptografia",
                "ja": "暗号化",
                "ko": "암호화",
                "zh": "加密",
                "ar": "التشفير",
            },
            "key management": {
                "en": "key management",
                "es": "gestión de claves",
                "fr": "gestion des clés",
                "de": "Schlüsselverwaltung",
                "it": "gestione delle chiavi",
                "pt": "gerenciamento de chaves",
                "ja": "鍵管理",
                "ko": "키 관리",
                "zh": "密钥管理",
                "ar": "إدارة المفاتيح",
            },
            "GDPR": {
                "en": "GDPR",
                "es": "GDPR",
                "fr": "RGPD",
                "de": "DSGVO",
                "it": "GDPR",
                "pt": "GDPR",
                "ja": "GDPR",
                "ko": "GDPR",
                "zh": "GDPR",
                "ar": "GDPR",
            },
            "HIPAA": {
                "en": "HIPAA",
                "es": "HIPAA",
                "fr": "HIPAA",
                "de": "HIPAA",
                "it": "HIPAA",
                "pt": "HIPAA",
                "ja": "HIPAA",
                "ko": "HIPAA",
                "zh": "HIPAA",
                "ar": "HIPAA",
            },
        }

    def translate_note(
        self, note: ComplianceNote, target_language: str
    ) -> TranslatedNote:
        """
        Translate a compliance note using AWS Translate.

        Args:
            note: ComplianceNote object
            target_language: Target language code (e.g., 'es', 'fr', 'de')

        Returns:
            TranslatedNote object
        """
        if target_language not in self.supported_languages:
            raise ValueError(
                f"Unsupported language: {target_language}. Supported: {self.supported_languages}"
            )

        if note.language == target_language:
            # Already in target language
            return TranslatedNote(
                original_note=note,
                translated_content=note.content,
                target_language=target_language,
                translation_confidence=1.0,
                provider="no_translation_needed",
            )

        try:
            # Use AWS Translate
            response = self.translate.translate_text(
                Text=note.content,
                SourceLanguageCode=note.language,
                TargetLanguageCode=target_language,
                TerminologyNames=["ComplianceTerms"] if self._has_terminology() else [],
            )

            translated_text = response["TranslatedText"]

            # Calculate confidence (simplified - AWS doesn't provide confidence scores)
            # We'll use a placeholder or analyze text quality
            confidence = self._estimate_translation_confidence(
                note.content, translated_text
            )

            return TranslatedNote(
                original_note=note,
                translated_content=translated_text,
                target_language=target_language,
                translation_confidence=confidence,
                provider="aws_translate",
            )

        except ClientError as e:
            raise Exception(f"AWS Translate failed: {e}")

    def translate_batch(
        self, notes: List[ComplianceNote], target_language: str
    ) -> List[TranslatedNote]:
        """
        Translate multiple compliance notes.

        Args:
            notes: List of ComplianceNote objects
            target_language: Target language code

        Returns:
            List of TranslatedNote objects
        """
        translated_notes = []

        for note in notes:
            try:
                translated_note = self.translate_note(note, target_language)
                translated_notes.append(translated_note)
            except Exception as e:
                # Create error note for failed translations
                error_note = TranslatedNote(
                    original_note=note,
                    translated_content=f"[Translation failed: {str(e)}]",
                    target_language=target_language,
                    translation_confidence=0.0,
                    provider="error",
                )
                translated_notes.append(error_note)

        return translated_notes

    def translate_for_multiple_reviewers(
        self, note: ComplianceNote, reviewer_languages: List[str]
    ) -> Dict[str, TranslatedNote]:
        """
        Translate a note for multiple reviewers with different languages.

        Args:
            note: ComplianceNote object
            reviewer_languages: List of target language codes

        Returns:
            Dictionary mapping language codes to TranslatedNote objects
        """
        translations = {}

        for lang in reviewer_languages:
            try:
                translated = self.translate_note(note, lang)
                translations[lang] = translated
            except Exception as e:
                translations[lang] = TranslatedNote(
                    original_note=note,
                    translated_content=f"[Translation to {lang} failed: {str(e)}]",
                    target_language=lang,
                    translation_confidence=0.0,
                    provider="error",
                )

        return translations

    def generate_compliance_summary(
        self, notes: List[ComplianceNote], target_language: str = "en"
    ) -> Dict[str, Any]:
        """
        Generate a translated summary of compliance notes.

        Args:
            notes: List of ComplianceNote objects
            target_language: Language for summary

        Returns:
            Summary dictionary
        """
        if not notes:
            return {
                "summary": "No compliance notes available",
                "language": target_language,
                "provider": "aws_translate",
            }

        # Categorize notes
        categories = {}
        severities = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        regulations = {}

        for note in notes:
            # Count by category
            cat = note.category
            categories[cat] = categories.get(cat, 0) + 1

            # Count by severity
            sev = note.severity.lower()
            if sev in severities:
                severities[sev] += 1

            # Count by regulation
            if note.regulation:
                regulations[note.regulation] = regulations.get(note.regulation, 0) + 1

        # Create summary text
        summary_text = f"""
        Compliance Notes Summary:
        - Total notes: {len(notes)}
        - Categories: {", ".join(f"{k}: {v}" for k, v in categories.items())}
        - Severities: {", ".join(f"{k}: {v}" for k, v in severities.items() if v > 0)}
        - Regulations: {", ".join(f"{k}: {v}" for k, v in regulations.items()) if regulations else "None specified"}
        
        Most common category: {max(categories.items(), key=lambda x: x[
                1
            ])[0] if categories else "N/A"}
        Highest severity present: {max([s for s, c in severities.items() if c > 0], key=lambda x: (
                ["low", "medium", "high", "critical"].index(x)
            )) if any(severities.values()) else "N/A"}
        """

        # Translate summary if needed
        if target_language != "en":
            try:
                translated_summary = self.translate.translate_text(
                    Text=summary_text,
                    SourceLanguageCode="en",
                    TargetLanguageCode=target_language,
                )
                summary_text = translated_summary["TranslatedText"]
                translation_provider = "aws_translate"
            except Exception as e:
                translation_provider = f"error: {str(e)}"
        else:
            translation_provider = "original"

        return {
            "summary": summary_text.strip(),
            "language": target_language,
            "total_notes": len(notes),
            "categories": categories,
            "severities": severities,
            "regulations": regulations,
            "provider": translation_provider,
        }

    def create_reviewer_package(
        self, notes: List[ComplianceNote], reviewer_language: str
    ) -> Dict[str, Any]:
        """
        Create a complete package for a reviewer with translated notes.

        Args:
            notes: List of ComplianceNote objects
            reviewer_language: Reviewer's language

        Returns:
            Reviewer package dictionary
        """
        # Translate notes
        translated_notes = self.translate_batch(notes, reviewer_language)

        # Generate summary
        summary = self.generate_compliance_summary(notes, reviewer_language)

        # Calculate translation statistics
        successful_translations = [
            tn
            for tn in translated_notes
            if tn.provider not in ["error", "no_translation_needed"]
        ]
        avg_confidence = (
            sum(tn.translation_confidence for tn in successful_translations)
            / len(successful_translations)
            if successful_translations
            else 0
        )

        return {
            "reviewer_language": reviewer_language,
            "package_created": os.getenv("REQUEST_TIMESTAMP", ""),
            "total_notes": len(notes),
            "translated_notes": len(translated_notes),
            "translation_success_rate": len(successful_translations) / len(notes)
            if notes
            else 0,
            "average_confidence": round(avg_confidence, 2),
            "summary": summary,
            "notes": [tn.to_dict() for tn in translated_notes],
            "provider": "aws_translate",
        }

    def _has_terminology(self) -> bool:
        """Check if compliance terminology exists in AWS Translate."""
        try:
            response = self.translate.list_terminologies(MaxResults=10)
            terminology_names = [
                t["Name"] for t in response.get("TerminologyPropertiesList", [])
            ]
            return "ComplianceTerms" in terminology_names
        except:
            return False

    def _estimate_translation_confidence(self, original: str, translated: str) -> float:
        """
        Estimate translation confidence based on text analysis.

        Args:
            original: Original text
            translated: Translated text

        Returns:
            Confidence score between 0 and 1
        """
        # Simple heuristic: ratio of lengths (adjusted)
        orig_len = len(original.split())
        trans_len = len(translated.split())

        if orig_len == 0:
            return 1.0

        length_ratio = min(trans_len / orig_len, 2.0) / 2.0  # Normalize to 0-1

        # Check for common error patterns
        error_indicators = [
            "[ERROR]",
            "[FAILED]",
            "Translation failed",
            "Untranslated text",
        ]
        has_errors = any(indicator in translated for indicator in error_indicators)

        if has_errors:
            return 0.1

        # Base confidence on length ratio with some adjustment
        confidence = 0.3 + (length_ratio * 0.7)

        return min(max(confidence, 0.0), 1.0)


if __name__ == "__main__":
    translator = ComplianceNoteTranslator()

    # Create sample compliance notes
    notes = [
        ComplianceNote(
            note_id="note-001",
            content="Encryption key rotation was performed successfully for all production systems. AES-256-GCM algorithm used.",
            language="en",
            category="key management",
            severity="medium",
            regulation="PCI DSS",
            timestamp="2024-01-15T10:30:00Z",
        ),
        ComplianceNote(
            note_id="note-002",
            content="Audit found that data at rest encryption is not enabled for backup storage. Immediate action required.",
            language="en",
            category="encryption",
            severity="high",
            regulation="GDPR",
            timestamp="2024-01-15T11:15:00Z",
        ),
        ComplianceNote(
            note_id="note-003",
            content="Quarterly review of cryptographic controls completed. All controls are operating effectively.",
            language="en",
            category="compliance",
            severity="low",
            regulation="HIPAA",
            timestamp="2024-01-15T12:00:00Z",
        ),
    ]

    # Translate a single note to Spanish
    translated_note = translator.translate_note(notes[0], "es")
    print(
        f"Translated note to Spanish: {json.dumps(translated_note.to_dict(), indent=2)}"
    )

    # Generate reviewer package for French reviewer
    reviewer_package = translator.create_reviewer_package(notes, "fr")
    print(f"\nFrench reviewer package: {json.dumps(reviewer_package, indent=2)}")

    # Generate compliance summary
    summary = translator.generate_compliance_summary(notes, "de")
    print(f"\nGerman compliance summary: {json.dumps(summary, indent=2)}")
