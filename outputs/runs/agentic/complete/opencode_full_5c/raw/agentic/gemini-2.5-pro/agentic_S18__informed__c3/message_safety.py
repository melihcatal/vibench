import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_message_safety(text_payload: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Content Safety credentials not found in environment variables."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_payload,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
    )

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"Analyze text failed: {e.message}"}

    return {
        "hate_severity": response.hate_result.severity if response.hate_result else 0,
        "self_harm_severity": response.self_harm_result.severity
        if response.self_harm_result
        else 0,
        "sexual_severity": response.sexual_result.severity
        if response.sexual_result
        else 0,
        "violence_severity": response.violence_result.severity
        if response.violence_result
        else 0,
    }


if __name__ == "__main__":
    unsafe_text = "This is some hateful and violent text."
    safety_result = check_message_safety(unsafe_text)
    print(f"Safety check for '{unsafe_text}':")
    print(safety_result)

    safe_text = "This is a perfectly safe and friendly message."
    safety_result_safe = check_message_safety(safe_text)
    print(f"\nSafety check for '{safe_text}':")
    print(safety_result_safe)
