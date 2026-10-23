from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import safety_clients_config
from safety_models import ModerationInput, RedactionResult

def redact_unsafe(input_data: ModerationInput) -> RedactionResult:
    """
    Flags unsafe spans from text using Azure AI Content Safety.
    Note: The current Python SDK does not easily expose offsets for redaction of
    harmful content, so this function primarily flags content.
    """
    key = safety_clients_config.AZURE_CONTENT_SAFETY_KEY
    endpoint = safety_clients_config.AZURE_CONTENT_SAFETY_ENDPOINT

    if not key or not endpoint:
        raise ValueError("Azure Content Safety key or endpoint is not configured.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    try:
        request = AnalyzeTextOptions(text=input_data.text)
        response = client.analyze_text(request)

        flagged = False
        
        for category in [
            response.hate_result,
            response.self_harm_result,
            response.sexual_result,
            response.violence_result,
        ]:
            if category and category.severity > 0:
                flagged = True
                break

        # Actual redaction would require parsing offsets, which are not
        # directly provided for these categories in the current SDK version.
        # For now, we return the original text and a flag.
        return RedactionResult(
            original_text=input_data.text,
            redacted_text=input_data.text,
            flagged=flagged,
        )

    except HttpResponseError:
        return RedactionResult(
            original_text=input_data.text,
            redacted_text=input_data.text,
            flagged=True
        )
