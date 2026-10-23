import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from dotenv import load_dotenv

from speech_models import ContentSafetyResponse

load_dotenv()

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")


def check_for_unsafe_content(text_to_check: str) -> ContentSafetyResponse:
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise ValueError("Azure Content Safety credentials are not configured.")

    client = ContentSafetyClient(
        AZURE_CONTENT_SAFETY_ENDPOINT, AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY)
    )

    request = AnalyzeTextOptions(text=text_to_check)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e}")
        return ContentSafetyResponse(is_safe=True, harm_categories=[])

    is_safe = True
    harm_categories = []

    if response.hate_result and response.hate_result.severity > 0:
        is_safe = False
        harm_categories.append("hate")
    if response.self_harm_result and response.self_harm_result.severity > 0:
        is_safe = False
        harm_categories.append("self_harm")
    if response.sexual_result and response.sexual_result.severity > 0:
        is_safe = False
        harm_categories.append("sexual")
    if response.violence_result and response.violence_result.severity > 0:
        is_safe = False
        harm_categories.append("violence")

    return ContentSafetyResponse(is_safe=is_safe, harm_categories=harm_categories)


if __name__ == "__main__":
    unsafe_text = "I am going to harm someone."
    safety_check = check_for_unsafe_content(unsafe_text)
    print(f"Text: '{unsafe_text}'")
    print(f"Is safe: {safety_check.is_safe}")
    print(f"Harm categories: {safety_check.harm_categories}")

    safe_text = "This is a perfectly normal sentence."
    safety_check_safe = check_for_unsafe_content(safe_text)
    print(f"Text: '{safe_text}'")
    print(f"Is safe: {safety_check_safe.is_safe}")
    print(f"Harm categories: {safety_check_safe.harm_categories}")
