import os
import json
from typing import Dict, List, Any, Optional
import boto3
from botocore.exceptions import ClientError
from google.cloud import translate_v2 as translate
from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text.models import InputTextItem
from azure.core.credentials import AzureKeyCredential


class ComplianceNoteTranslator:
    """Translate encryption or compliance notes for reviewers using various providers."""

    def __init__(self):
        self.aws_region = os.environ.get("AWS_REGION", "us-east-1")
        self.gcp_project_id = os.environ.get("GCP_PROJECT_ID", "my-project")
        self.azure_translator_key = os.environ.get("AZURE_TRANSLATOR_KEY", "")
        self.azure_translator_endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT", "")
        self.azure_translator_region = os.environ.get(
            "AZURE_TRANSLATOR_REGION", "global"
        )

    def translate_text(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None,
        provider: str = "aws",
        **kwargs,
    ) -> Dict:
        """
        Translate text to target language.

        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'es', 'fr', 'de')
            source_language: Optional source language code
            provider: 'aws', 'gcp', 'azure', or 'deepl'
            **kwargs: Provider-specific arguments

        Returns:
            Translation result
        """
        if not text:
            return {
                "original_text": "",
                "translated_text": "",
                "target_language": target_language,
                "provider": provider,
                "success": False,
                "error": "Empty text",
            }

        if provider.lower() == "aws":
            return self._translate_with_aws(
                text, target_language, source_language, **kwargs
            )
        elif provider.lower() == "gcp":
            return self._translate_with_gcp(
                text, target_language, source_language, **kwargs
            )
        elif provider.lower() == "azure":
            return self._translate_with_azure(
                text, target_language, source_language, **kwargs
            )
        elif provider.lower() == "deepl":
            return self._translate_with_deepl(
                text, target_language, source_language, **kwargs
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _translate_with_aws(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None,
        **kwargs,
    ) -> Dict:
        """Translate using AWS Translate."""
        translate_client = boto3.client("translate", region_name=self.aws_region)

        try:
            # Prepare request
            request_params = {
                "Text": text,
                "SourceLanguageCode": source_language or "auto",
                "TargetLanguageCode": target_language,
            }

            # Add terminology if provided
            terminology_names = kwargs.get("terminology_names")
            if terminology_names:
                request_params["TerminologyNames"] = terminology_names

            # Make translation request
            response = translate_client.translate_text(**request_params)

            return {
                "original_text": text,
                "translated_text": response["TranslatedText"],
                "source_language": response.get(
                    "SourceLanguageCode", source_language or "auto"
                ),
                "target_language": target_language,
                "provider": "aws_translate",
                "applied_terminologies": response.get("AppliedTerminologies", []),
                "success": True,
            }

        except ClientError as e:
            return {
                "original_text": text,
                "translated_text": "",
                "target_language": target_language,
                "provider": "aws_translate",
                "success": False,
                "error": str(e),
            }

    def _translate_with_gcp(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None,
        **kwargs,
    ) -> Dict:
        """Translate using Google Cloud Translation."""
        try:
            # Initialize translation client
            translate_client = translate.Client()

            # Prepare request
            if source_language:
                result = translate_client.translate(
                    text,
                    target_language=target_language,
                    source_language=source_language,
                    format_="text",
                )
            else:
                result = translate_client.translate(
                    text, target_language=target_language, format_="text"
                )

            return {
                "original_text": text,
                "translated_text": result["translatedText"],
                "source_language": result.get(
                    "detectedSourceLanguage", source_language
                ),
                "target_language": target_language,
                "provider": "gcp_translate",
                "success": True,
            }

        except Exception as e:
            return {
                "original_text": text,
                "translated_text": "",
                "target_language": target_language,
                "provider": "gcp_translate",
                "success": False,
                "error": str(e),
            }

    def _translate_with_azure(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None,
        **kwargs,
    ) -> Dict:
        """Translate using Azure Translator."""
        if not self.azure_translator_key or not self.azure_translator_endpoint:
            return {
                "original_text": text,
                "translated_text": "",
                "target_language": target_language,
                "provider": "azure_translator",
                "success": False,
                "error": "Missing Azure Translator credentials",
            }

        try:
            # Initialize Azure Translator client
            credential = AzureKeyCredential(self.azure_translator_key)
            client = TextTranslationClient(
                endpoint=self.azure_translator_endpoint,
                credential=credential,
                region=self.azure_translator_region,
            )

            # Prepare input
            input_text = InputTextItem(text=text)

            # Make translation request
            if source_language:
                response = client.translate(
                    content=[input_text],
                    to=[target_language],
                    from_parameter=source_language,
                )
            else:
                response = client.translate(content=[input_text], to=[target_language])

            # Extract translation
            translation = response[0] if response else None
            if translation and translation.translations:
                translated_text = translation.translations[0].text
                detected_language = (
                    translation.detected_language.language
                    if translation.detected_language
                    else source_language
                )

                return {
                    "original_text": text,
                    "translated_text": translated_text,
                    "source_language": detected_language,
                    "target_language": target_language,
                    "provider": "azure_translator",
                    "success": True,
                }
            else:
                return {
                    "original_text": text,
                    "translated_text": "",
                    "target_language": target_language,
                    "provider": "azure_translator",
                    "success": False,
                    "error": "No translation returned",
                }

        except Exception as e:
            return {
                "original_text": text,
                "translated_text": "",
                "target_language": target_language,
                "provider": "azure_translator",
                "success": False,
                "error": str(e),
            }

    def _translate_with_deepl(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None,
        **kwargs,
    ) -> Dict:
        """Translate using DeepL (requires DeepL API key)."""
        deepl_api_key = os.environ.get("DEEPL_API_KEY", "")

        if not deepl_api_key:
            return {
                "original_text": text,
                "translated_text": "",
                "target_language": target_language,
                "provider": "deepl",
                "success": False,
                "error": "Missing DeepL API key",
            }

        try:
            import deepl

            # Initialize DeepL translator
            translator = deepl.Translator(deepl_api_key)

            # Prepare request
            if source_language:
                result = translator.translate_text(
                    text,
                    source_lang=source_language.upper(),
                    target_lang=target_language.upper(),
                )
            else:
                result = translator.translate_text(
                    text, target_lang=target_language.upper()
                )

            return {
                "original_text": text,
                "translated_text": result.text,
                "source_language": result.detected_source_lang
                if hasattr(result, "detected_source_lang")
                else source_language,
                "target_language": target_language,
                "provider": "deepl",
                "success": True,
            }

        except Exception as e:
            return {
                "original_text": text,
                "translated_text": "",
                "target_language": target_language,
                "provider": "deepl",
                "success": False,
                "error": str(e),
            }

    def translate_compliance_note(
        self, note: Dict, target_language: str, provider: str = "aws"
    ) -> Dict:
        """
        Translate a compliance note for reviewers.

        Args:
            note: Compliance note dictionary
            target_language: Target language code
            provider: Translation provider

        Returns:
            Translated note
        """
        # Extract text fields for translation
        fields_to_translate = {}

        if "title" in note:
            fields_to_translate["title"] = note["title"]

        if "description" in note:
            fields_to_translate["description"] = note["description"]

        if "findings" in note:
            if isinstance(note["findings"], str):
                fields_to_translate["findings"] = note["findings"]
            elif isinstance(note["findings"], list):
                fields_to_translate["findings"] = " ".join(note["findings"])

        if "recommendations" in note:
            if isinstance(note["recommendations"], str):
                fields_to_translate["recommendations"] = note["recommendations"]
            elif isinstance(note["recommendations"], list):
                fields_to_translate["recommendations"] = " ".join(
                    note["recommendations"]
                )

        if "compliance_requirements" in note:
            if isinstance(note["compliance_requirements"], str):
                fields_to_translate["compliance_requirements"] = note[
                    "compliance_requirements"
                ]
            elif isinstance(note["compliance_requirements"], list):
                fields_to_translate["compliance_requirements"] = " ".join(
                    note["compliance_requirements"]
                )

        # Translate each field
        translations = {}
        for field_name, field_text in fields_to_translate.items():
            translation_result = self.translate_text(
                field_text, target_language, provider=provider
            )

            translations[field_name] = {
                "original": field_text,
                "translated": translation_result.get("translated_text", ""),
                "success": translation_result.get("success", False),
                "source_language": translation_result.get("source_language", ""),
                "provider": translation_result.get("provider", ""),
            }

        # Create translated note
        translated_note = {
            "id": note.get("id", ""),
            "original_language": note.get("language", "en"),
            "target_language": target_language,
            "timestamp": note.get("timestamp", ""),
            "operation": note.get("operation", ""),
            "key_id": note.get("key_id", ""),
            "provider": note.get("provider", ""),
            "translation_provider": provider,
            "translations": translations,
            "metadata": {
                "translated_at": os.environ.get("TIMESTAMP", "2024-01-01T00:00:00Z"),
                "reviewer_accessible": True,
            },
        }

        # Add non-translated fields
        for key, value in note.items():
            if key not in fields_to_translate and key not in [
                "id",
                "timestamp",
                "operation",
                "key_id",
                "provider",
                "language",
            ]:
                translated_note[key] = value

        return translated_note

    def batch_translate_notes(
        self, notes: List[Dict], target_language: str, provider: str = "aws"
    ) -> List[Dict]:
        """
        Translate multiple compliance notes.

        Args:
            notes: List of compliance notes
            target_language: Target language code
            provider: Translation provider

        Returns:
            List of translated notes
        """
        translated_notes = []

        for note in notes:
            try:
                translated_note = self.translate_compliance_note(
                    note, target_language, provider
                )
                translated_notes.append(translated_note)
            except Exception as e:
                # Create error entry for failed translation
                error_note = {
                    "id": note.get("id", ""),
                    "error": str(e),
                    "original_note": note,
                    "target_language": target_language,
                    "success": False,
                }
                translated_notes.append(error_note)

        return translated_notes

    def get_supported_languages(self, provider: str = "aws") -> Dict:
        """
        Get supported languages for translation provider.

        Args:
            provider: Translation provider

        Returns:
            Dict with supported languages
        """
        if provider.lower() == "aws":
            return self._get_aws_supported_languages()
        elif provider.lower() == "gcp":
            return self._get_gcp_supported_languages()
        elif provider.lower() == "azure":
            return self._get_azure_supported_languages()
        elif provider.lower() == "deepl":
            return self._get_deepl_supported_languages()
        else:
            return {
                "provider": provider,
                "supported_languages": [],
                "error": f"Unsupported provider: {provider}",
            }

    def _get_aws_supported_languages(self) -> Dict:
        """Get AWS Translate supported languages."""
        translate_client = boto3.client("translate", region_name=self.aws_region)

        try:
            response = translate_client.list_languages()

            languages = []
            for language in response["Languages"]:
                languages.append(
                    {
                        "code": language["LanguageCode"],
                        "name": language.get("LanguageName", ""),
                    }
                )

            return {
                "provider": "aws_translate",
                "supported_languages": languages,
                "count": len(languages),
            }

        except ClientError as e:
            return {
                "provider": "aws_translate",
                "supported_languages": [],
                "error": str(e),
            }

    def _get_gcp_supported_languages(self) -> Dict:
        """Get Google Cloud Translation supported languages."""
        try:
            translate_client = translate.Client()
            languages = translate_client.get_languages()

            return {
                "provider": "gcp_translate",
                "supported_languages": languages,
                "count": len(languages),
            }

        except Exception as e:
            return {
                "provider": "gcp_translate",
                "supported_languages": [],
                "error": str(e),
            }

    def _get_azure_supported_languages(self) -> Dict:
        """Get Azure Translator supported languages."""
        if not self.azure_translator_key or not self.azure_translator_endpoint:
            return {
                "provider": "azure_translator",
                "supported_languages": [],
                "error": "Missing Azure Translator credentials",
            }

        try:
            credential = AzureKeyCredential(self.azure_translator_key)
            client = TextTranslationClient(
                endpoint=self.azure_translator_endpoint,
                credential=credential,
                region=self.azure_translator_region,
            )

            response = client.get_languages()

            languages = []
            for code, info in response.translation.items():
                languages.append(
                    {"code": code, "name": info.name, "native_name": info.native_name}
                )

            return {
                "provider": "azure_translator",
                "supported_languages": languages,
                "count": len(languages),
            }

        except Exception as e:
            return {
                "provider": "azure_translator",
                "supported_languages": [],
                "error": str(e),
            }

    def _get_deepl_supported_languages(self) -> Dict:
        """Get DeepL supported languages."""
        deepl_api_key = os.environ.get("DEEPL_API_KEY", "")

        if not deepl_api_key:
            return {
                "provider": "deepl",
                "supported_languages": [],
                "error": "Missing DeepL API key",
            }

        try:
            import deepl

            translator = deepl.Translator(deepl_api_key)
            languages = translator.get_target_languages()

            language_list = []
            for lang in languages:
                language_list.append({"code": lang.code, "name": lang.name})

            return {
                "provider": "deepl",
                "supported_languages": language_list,
                "count": len(language_list),
            }

        except Exception as e:
            return {"provider": "deepl", "supported_languages": [], "error": str(e)}

    def create_translation_summary(self, translations: List[Dict]) -> Dict:
        """
        Create summary of translation results.

        Args:
            translations: List of translation results

        Returns:
            Translation summary
        """
        total = len(translations)
        successful = sum(1 for t in translations if t.get("success", False))
        failed = total - successful

        # Count by provider
        providers = {}
        for translation in translations:
            provider = translation.get("provider", "unknown")
            providers[provider] = providers.get(provider, 0) + 1

        # Count by target language
        languages = {}
        for translation in translations:
            lang = translation.get("target_language", "unknown")
            languages[lang] = languages.get(lang, 0) + 1

        return {
            "total_translations": total,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "providers": providers,
            "target_languages": languages,
            "generated_at": os.environ.get("TIMESTAMP", "2024-01-01T00:00:00Z"),
        }
