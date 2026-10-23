import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def check_corpus_safety(text: str) -> dict:
    """
    Checks the safety of corpus text before embedding using Azure AI Content Safety.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY must be set in environment variables."
        )

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(
        text=text,
        categories=[
            TextCategory.VIOLENCE,
            TextCategory.HATE_SPEECH,
            TextCategory.SEXUAL,
            TextCategory.SELF_HARM,
        ],
    )

    response = client.analyze_text(request)

    safety_results = {
        "hate_speech": {"severity": response.hate_result.severity},
        "self_harm": {"severity": response.self_harm_result.severity},
        "sexual": {"severity": response.sexual_result.severity},
        "violence": {"severity": response.violence_result.severity},
    }
    return safety_results


if __name__ == "__main__":
    # Example usage (replace with actual text to check)
    text_to_check_safe = "This is a perfectly safe document about scientific research."
    text_to_check_unsafe = "I hate everyone and want to hurt them."

    print(f"Checking safety for: '{text_to_check_safe}'")
    results_safe = check_corpus_safety(text_to_check_safe)
    print(results_safe)

    print(f"Checking safety for: '{text_to_check_unsafe}'")
    results_unsafe = check_corpus_safety(text_to_check_unsafe)
    print(results_unsafe)
