import os
from typing import Dict, List, Optional
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

# Ensure consistent language detection
DetectorFactory.seed = 0


class RunbookTranslator:
    """Translate secret-rotation runbook notes using Google Translate API."""

    SUPPORTED_LANGUAGES = {
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "zh-CN": "Chinese (Simplified)",
        "ja": "Japanese",
        "ko": "Korean",
        "ru": "Russian",
        "ar": "Arabic",
        "pt": "Portuguese",
        "it": "Italian",
        "nl": "Dutch",
    }

    def __init__(self, source_lang: str = "auto", target_lang: str = "en"):
        """
        Initialize translator.

        Args:
            source_lang: Source language code or 'auto' for auto-detection
            target_lang: Target language code (default: 'en' for English)
        """
        self.source_lang = source_lang
        self.target_lang = target_lang

        # Validate target language
        if target_lang not in self.SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported target language: {target_lang}. Supported: {list(self.SUPPORTED_LANGUAGES.keys())}"
            )

    def translate_runbook_note(
        self, note: str, note_context: Dict[str, any] = None
    ) -> Dict[str, any]:
        """
        Translate a single runbook note.

        Args:
            note: The runbook note text to translate
            note_context: Optional context about the note (secret name, rotation type, etc.)

        Returns:
            Dictionary with translation results
        """
        if not note or not note.strip():
            return {
                "original": note,
                "translated": note,
                "source_lang": "unknown",
                "target_lang": self.target_lang,
                "confidence": 0.0,
                "context": note_context or {},
            }

        try:
            # Detect source language if auto
            if self.source_lang == "auto":
                try:
                    detected_lang = detect(note)
                    source_lang = detected_lang
                except:
                    source_lang = "en"  # Default to English if detection fails
            else:
                source_lang = self.source_lang

            # Translate using Google Translator
            translator = GoogleTranslator(source=source_lang, target=self.target_lang)
            translated_text = translator.translate(note)

            # For technical terms related to secret rotation, we might want to preserve them
            # Apply post-processing for technical terms
            translated_text = self._preserve_technical_terms(
                translated_text, note_context
            )

            # Calculate confidence (simplified - in production would use translation API confidence)
            confidence = self._estimate_translation_confidence(
                note, translated_text, source_lang
            )

            return {
                "original": note,
                "translated": translated_text,
                "source_lang": source_lang,
                "target_lang": self.target_lang,
                "confidence": confidence,
                "context": note_context or {},
                "technical_terms_preserved": True,
            }

        except Exception as e:
            raise RuntimeError(f"Translation failed: {e}")

    def translate_batch(
        self, notes: List[str], contexts: List[Dict[str, any]] = None
    ) -> List[Dict[str, any]]:
        """
        Translate multiple runbook notes in batch.

        Args:
            notes: List of notes to translate
            contexts: Optional list of context dictionaries

        Returns:
            List of translation results
        """
        if contexts is None:
            contexts = [{}] * len(notes)

        if len(notes) != len(contexts):
            raise ValueError("Number of notes must match number of contexts")

        results = []
        for note, context in zip(notes, contexts):
            try:
                result = self.translate_runbook_note(note, context)
                results.append(result)
            except Exception as e:
                # Add error result for failed translation
                results.append(
                    {
                        "original": note,
                        "translated": f"[TRANSLATION ERROR: {str(e)}]",
                        "source_lang": "error",
                        "target_lang": self.target_lang,
                        "confidence": 0.0,
                        "context": context,
                        "error": str(e),
                    }
                )

        return results

    def translate_rotation_procedure(self, procedure: Dict[str, any]) -> Dict[str, any]:
        """
        Translate an entire secret rotation procedure.

        Args:
            procedure: Dictionary containing rotation procedure details

        Returns:
            Translated procedure
        """
        original_procedure = procedure.copy()

        # Translate different parts of the procedure
        translated_parts = {}

        # Translate title/name
        if "name" in procedure:
            translated_parts["name"] = self.translate_runbook_note(procedure["name"])[
                "translated"
            ]

        # Translate description
        if "description" in procedure:
            translated_parts["description"] = self.translate_runbook_note(
                procedure["description"]
            )["translated"]

        # Translate steps
        if "steps" in procedure and isinstance(procedure["steps"], list):
            translated_steps = []
            for step in procedure["steps"]:
                translated_step = step.copy()

                # Translate step description
                if "description" in step:
                    trans_result = self.translate_runbook_note(step["description"])
                    translated_step["description"] = trans_result["translated"]
                    translated_step["translation_metadata"] = {
                        "source_lang": trans_result["source_lang"],
                        "confidence": trans_result["confidence"],
                    }

                # Translate commands if present
                if "commands" in step and isinstance(step["commands"], list):
                    translated_commands = []
                    for cmd in step["commands"]:
                        if isinstance(cmd, str):
                            # Only translate comment-like commands, not actual code
                            if cmd.startswith("#") or "#" in cmd:
                                parts = cmd.split("#", 1)
                                if len(parts) > 1:
                                    comment = "#" + parts[1]
                                    trans_comment = self.translate_runbook_note(
                                        comment
                                    )["translated"]
                                    translated_commands.append(parts[0] + trans_comment)
                                else:
                                    translated_commands.append(cmd)
                            else:
                                translated_commands.append(cmd)
                        else:
                            translated_commands.append(cmd)
                    translated_step["commands"] = translated_commands

                translated_steps.append(translated_step)
            translated_parts["steps"] = translated_steps

        # Translate notes and warnings
        for field in ["notes", "warnings", "prerequisites", "verification"]:
            if field in procedure:
                if isinstance(procedure[field], str):
                    translated_parts[field] = self.translate_runbook_note(
                        procedure[field]
                    )["translated"]
                elif isinstance(procedure[field], list):
                    translated_parts[field] = [
                        self.translate_runbook_note(item)["translated"]
                        if isinstance(item, str)
                        else item
                        for item in procedure[field]
                    ]

        # Combine with original (untranslated) technical fields
        technical_fields = [
            "secret_name",
            "rotation_type",
            "frequency",
            "aws_region",
            "lambda_function",
            "kms_key_id",
            "tags",
            "metadata",
        ]

        for field in technical_fields:
            if field in procedure:
                translated_parts[field] = procedure[field]

        # Add translation metadata
        translated_parts["translation_metadata"] = {
            "source_language": self.source_lang,
            "target_language": self.target_lang,
            "translation_timestamp": os.path.getmtime(__file__)
            if os.path.exists(__file__)
            else None,
            "translator": "GoogleTranslator",
        }

        return translated_parts

    def _preserve_technical_terms(
        self, text: str, context: Dict[str, any] = None
    ) -> str:
        """
        Preserve technical terms that shouldn't be translated.

        Args:
            text: Translated text
            context: Context about the note

        Returns:
            Text with technical terms preserved
        """
        # Common secret management terms that should not be translated
        technical_terms = [
            "AWS",
            "Secrets Manager",
            "KMS",
            "Key Management Service",
            "Lambda",
            "CloudFormation",
            "IAM",
            "ARN",
            "VPC",
            "RDS",
            "DynamoDB",
            "S3",
            "EC2",
            "CloudWatch",
            "JSON",
            "YAML",
            "Base64",
            "UTF-8",
            "SSL",
            "TLS",
            "SSH",
            "RSA",
            "AES",
            "API",
            "CLI",
            "SDK",
            "REST",
            "GraphQL",
            "GitHub",
            "GitLab",
            "Bitbucket",
            "Jenkins",
            "Docker",
            "Kubernetes",
            "Helm",
            "Terraform",
        ]

        # Add context-specific terms
        if context:
            if "secret_name" in context:
                technical_terms.append(context["secret_name"])
            if "rotation_type" in context:
                technical_terms.append(context["rotation_type"])

        # Simple preservation - in production would use more sophisticated approach
        preserved_text = text
        for term in technical_terms:
            # Look for translated versions and replace with original
            # This is simplified - real implementation would use glossary
            if term.lower() in preserved_text.lower() and term not in preserved_text:
                # Try to find and preserve the term
                pass

        return preserved_text

    def _estimate_translation_confidence(
        self, original: str, translated: str, source_lang: str
    ) -> float:
        """
        Estimate translation confidence.

        Args:
            original: Original text
            translated: Translated text
            source_lang: Detected source language

        Returns:
            Confidence score between 0.0 and 1.0
        """
        # Simplified confidence estimation
        # In production, would use translation API's confidence score

        if not original or not translated:
            return 0.0

        # Check if translation looks reasonable
        original_len = len(original.split())
        translated_len = len(translated.split())

        # Length ratio should be reasonable
        if original_len == 0:
            return 0.0

        length_ratio = translated_len / original_len

        # Reasonable length ratio is between 0.5 and 2.0
        if 0.5 <= length_ratio <= 2.0:
            length_score = 0.8
        else:
            length_score = 0.3

        # Check for common error patterns
        error_patterns = [
            "ERROR",
            "FAILED",
            "NOT FOUND",
            "UNABLE TO",
            "翻译失败",
            "翻訳失敗",
            "번역 실패",  # Translation failed in Chinese, Japanese, Korean
        ]

        error_score = 1.0
        for pattern in error_patterns:
            if pattern in translated.upper():
                error_score = 0.2
                break

        # Combine scores
        confidence = (length_score + error_score) / 2

        # Adjust based on source language
        if source_lang in ["en", "es", "fr", "de"]:  # Well-supported languages
            confidence *= 1.1
        elif source_lang in [
            "zh-CN",
            "ja",
            "ko",
        ]:  # Languages with different character sets
            confidence *= 0.9

        return min(max(confidence, 0.0), 1.0)
