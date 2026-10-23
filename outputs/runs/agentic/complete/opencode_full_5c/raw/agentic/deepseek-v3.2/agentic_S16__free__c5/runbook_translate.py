import os
import json
from typing import Dict, Any, List
import boto3
from botocore.exceptions import ClientError
import google.generativeai as genai


def runbook_translate(secret_name: str, target_language: str = "es") -> Dict[str, Any]:
    """
    Translate secret-rotation runbook notes using Google Gemini AI.

    Args:
        secret_name: Name of the secret in AWS Secrets Manager
        target_language: Target language code (e.g., 'es' for Spanish, 'fr' for French)

    Returns:
        Dictionary with original and translated runbook notes
    """
    # Initialize AWS Secrets Manager client
    session = boto3.session.Session()
    secrets_client = session.client(
        service_name="secretsmanager",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    # Initialize Google Gemini
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable is required")

    genai.configure(api_key=gemini_api_key)

    # Language mapping
    language_names = {
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese",
        "pt": "Portuguese",
        "ru": "Russian",
        "ar": "Arabic",
        "hi": "Hindi",
    }

    target_language_name = language_names.get(target_language, target_language)

    results = {
        "secret_name": secret_name,
        "target_language": target_language,
        "target_language_name": target_language_name,
        "has_runbook": False,
        "translations": {},
        "errors": [],
    }

    try:
        # Get secret details
        secret_response = secrets_client.describe_secret(SecretId=secret_name)

        # Extract tags for runbook information
        tags = secret_response.get("Tags", [])
        runbook_tags = {}
        rotation_notes = ""

        for tag in tags:
            key = tag["Key"]
            value = tag["Value"]

            # Look for runbook-related tags
            if (
                "runbook" in key.lower()
                or "rotation" in key.lower()
                or "procedure" in key.lower()
            ):
                runbook_tags[key] = value

            # Special handling for common runbook tags
            if key.lower() in [
                "runbook_url",
                "rotation_procedure_url",
                "procedure_url",
            ]:
                results["runbook_url"] = value

            if key.lower() in ["rotation_notes", "runbook_notes", "procedure_notes"]:
                rotation_notes = value

        if not runbook_tags and not rotation_notes:
            results["errors"].append("No runbook information found in secret tags")
            return results

        results["has_runbook"] = True
        results["original_tags"] = runbook_tags
        results["original_rotation_notes"] = rotation_notes

        # Prepare text for translation
        texts_to_translate = []

        # Add rotation notes if available
        if rotation_notes:
            texts_to_translate.append(
                {
                    "type": "rotation_notes",
                    "text": rotation_notes,
                    "context": "Secret rotation procedure notes",
                }
            )

        # Add tag key-value pairs
        for key, value in runbook_tags.items():
            texts_to_translate.append(
                {
                    "type": "tag",
                    "key": key,
                    "text": value,
                    "context": f"Secret tag: {key}",
                }
            )

        # Add secret metadata for context
        metadata_text = f"""
        Secret Name: {secret_name}
        Rotation Enabled: {secret_response.get("RotationEnabled", False)}
        Last Rotated: {secret_response.get("LastRotatedDate", "Never")}
        Description: {secret_response.get("Description", "No description")}
        """

        texts_to_translate.append(
            {
                "type": "metadata",
                "text": metadata_text.strip(),
                "context": "Secret metadata",
            }
        )

        # Translate each text using Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")

        translations = []

        for item in texts_to_translate:
            text_to_translate = item["text"]
            context = item["context"]

            if not text_to_translate or len(text_to_translate.strip()) == 0:
                continue

            # Prepare translation prompt
            prompt = f"""
            Translate the following text from English to {target_language_name} ({target_language}).
            
            Context: {context}
            
            Text to translate:
            {text_to_translate}
            
            Provide only the translation in {target_language_name}. Do not include any explanations, notes, or additional text.
            """

            try:
                response = model.generate_content(prompt)
                translated_text = response.text.strip()

                translations.append(
                    {
                        "type": item["type"],
                        "original_text": text_to_translate,
                        "translated_text": translated_text,
                        "context": context,
                        "key": item.get("key"),
                        "translation_confidence": "high",  # Gemini doesn't provide confidence scores
                    }
                )

            except Exception as e:
                results["errors"].append(
                    f"Translation error for {item['type']}: {str(e)}"
                )
                # Fallback: keep original text
                translations.append(
                    {
                        "type": item["type"],
                        "original_text": text_to_translate,
                        "translated_text": text_to_translate,  # Keep original as fallback
                        "context": context,
                        "key": item.get("key"),
                        "translation_confidence": "failed",
                        "error": str(e),
                    }
                )

        results["translations"] = translations

        # Generate comprehensive runbook translation
        if translations:
            # Combine all translations into a comprehensive runbook
            runbook_sections = []

            for trans in translations:
                if trans["type"] == "rotation_notes":
                    runbook_sections.append(
                        f"## Rotation Notes ({target_language_name})"
                    )
                    runbook_sections.append(trans["translated_text"])
                    runbook_sections.append("")
                elif trans["type"] == "tag" and trans["key"]:
                    runbook_sections.append(
                        f"### {trans['key']} ({target_language_name})"
                    )
                    runbook_sections.append(trans["translated_text"])
                    runbook_sections.append("")

            if runbook_sections:
                comprehensive_runbook = "\n".join(runbook_sections)
                results["comprehensive_runbook"] = comprehensive_runbook

            # Create a bilingual version
            bilingual_sections = []

            for trans in translations:
                if trans["type"] == "rotation_notes":
                    bilingual_sections.append("## Rotation Notes")
                    bilingual_sections.append("### English")
                    bilingual_sections.append(trans["original_text"])
                    bilingual_sections.append(f"### {target_language_name}")
                    bilingual_sections.append(trans["translated_text"])
                    bilingual_sections.append("")
                elif trans["type"] == "tag" and trans["key"]:
                    bilingual_sections.append(f"### {trans['key']}")
                    bilingual_sections.append("#### English")
                    bilingual_sections.append(trans["original_text"])
                    bilingual_sections.append(f"#### {target_language_name}")
                    bilingual_sections.append(trans["translated_text"])
                    bilingual_sections.append("")

            if bilingual_sections:
                bilingual_runbook = "\n".join(bilingual_sections)
                results["bilingual_runbook"] = bilingual_runbook

        # Add translation statistics
        successful_translations = [
            t for t in translations if t.get("translation_confidence") != "failed"
        ]
        failed_translations = [
            t for t in translations if t.get("translation_confidence") == "failed"
        ]

        results["translation_stats"] = {
            "total_texts": len(texts_to_translate),
            "successfully_translated": len(successful_translations),
            "failed_translations": len(failed_translations),
            "success_rate": round(
                (len(successful_translations) / len(texts_to_translate)) * 100, 1
            )
            if texts_to_translate
            else 0,
        }

        # Add recommendations
        recommendations = []

        if results["translation_stats"]["success_rate"] < 100:
            recommendations.append(
                f"Review {len(failed_translations)} failed translations"
            )

        if not results.get("runbook_url"):
            recommendations.append(
                "Consider adding a runbook_url tag for detailed procedures"
            )

        if len(texts_to_translate) < 3:
            recommendations.append(
                "Add more runbook information as tags (e.g., rotation_schedule, backup_procedure, rollback_steps)"
            )

        results["recommendations"] = recommendations

        return results

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ResourceNotFoundException":
            raise ValueError(f"Secret {secret_name} not found") from e
        elif error_code == "AccessDeniedException":
            raise PermissionError(f"Access denied to secret {secret_name}") from e
        else:
            raise RuntimeError(f"Error accessing secret: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error translating runbook: {e}") from e
