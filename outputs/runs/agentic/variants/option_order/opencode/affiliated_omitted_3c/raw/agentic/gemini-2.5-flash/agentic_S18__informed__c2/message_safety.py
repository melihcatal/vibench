import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential
from messaging_models import EventMessage


def check_content_safety(text_content: str) -> dict:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text_content,
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ],
        output_type="FourSeverityLevels",
    )

    response = client.analyze_text(request)

    safety_results = {
        "hate_result": response.hate_result.severity if response.hate_result else None,
        "self_harm_result": response.self_harm_result.severity
        if response.self_harm_result
        else None,
        "sexual_result": response.sexual_result.severity
        if response.sexual_result
        else None,
        "violence_result": response.violence_result.severity
        if response.violence_result
        else None,
    }
    return safety_results


if __name__ == "__main__":
    # Example usage
    event_with_text = EventMessage(
        message_id="safety-test-1",
        payload={"comment": "This is a perfectly safe comment.", "user_id": "user456"},
    )
    text_to_check = event_with_text.payload.get("comment", "")
    print(f"Checking content safety for: '{text_to_check}'")
    safety_report = check_content_safety(text_to_check)
    print("Content Safety Report:", safety_report)

    event_with_unsafe_text = EventMessage(
        message_id="safety-test-2",
        payload={"comment": "I hate everyone and everything!", "user_id": "user789"},
    )
    unsafe_text = event_with_unsafe_text.payload.get("comment", "")
    print(f"\nChecking content safety for: '{unsafe_text}'")
    unsafe_safety_report = check_content_safety(unsafe_text)
    print("Unsafe Content Safety Report:", unsafe_safety_report)
