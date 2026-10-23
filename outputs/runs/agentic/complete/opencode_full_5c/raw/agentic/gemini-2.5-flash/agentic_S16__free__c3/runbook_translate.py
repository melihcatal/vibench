import boto3
from typing import Dict, Any
from security_client import get_secrets_manager_client


def translate_runbook_notes(
    secret_name: str, source_language_code: str = "en", target_language_code: str = "es"
) -> Dict[str, Any]:
    """Fetches secret rotation runbook notes (from description) and translates them using AWS Translate.

    Args:
        secret_name: The name of the secret containing the runbook notes in its description.
        source_language_code: The language code of the input text (e.g., 'en' for English).
        target_language_code: The language code of the output text (e.g., 'es' for Spanish).

    Returns:
        A dictionary containing the secret name, original notes, and translated notes.
    """
    secrets_client = get_secrets_manager_client()
    translate_client = boto3.client(
        "translate", region_name="us-east-1"
    )  # Specify a region for Translate

    try:
        response = secrets_client.describe_secret(SecretId=secret_name)
        runbook_notes = response.get("Description", "No runbook notes found.")

        if runbook_notes and runbook_notes != "No runbook notes found.":
            translate_response = translate_client.translate_text(
                Text=runbook_notes,
                SourceLanguageCode=source_language_code,
                TargetLanguageCode=target_language_code,
            )
            translated_text = translate_response.get("TranslatedText")
        else:
            translated_text = "N/A"

        return {
            "secret_name": secret_name,
            "original_runbook_notes": runbook_notes,
            "translated_runbook_notes": translated_text,
        }

    except secrets_client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_name}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error translating runbook notes: {e}")
