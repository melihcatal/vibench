import os
from typing import List
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from observability_client import get_content_safety_client


def check_log_text_safety(log_messages: List[str]):
    client = get_content_safety_client()

    results = []
    for message in log_messages:
        request = AnalyzeTextOptions(text=message)
        # You can specify categories to check, e.g., hate, self_harm, sexual, violence
        # For a general check, we can rely on the default behavior or specify all known categories
        request.categories = [
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE,
        ]

        try:
            response = client.analyze_text(request)
            safety_result = {
                "message": message,
                "hate_result": response.hate_result.severity
                if response.hate_result
                else "N/A",
                "self_harm_result": response.self_harm_result.severity
                if response.self_harm_result
                else "N/A",
                "sexual_result": response.sexual_result.severity
                if response.sexual_result
                else "N/A",
                "violence_result": response.violence_result.severity
                if response.violence_result
                else "N/A",
            }
            results.append(safety_result)
        except Exception as e:
            results.append({"message": message, "error": str(e)})

    return results


if __name__ == "__main__":
    sample_log_messages = [
        "User logged in successfully.",
        "This is a test message with potentially harmful content like violence.",
        "System experienced a minor glitch.",
        "I hate this error so much it makes me want to scream.",
    ]

    # Ensure AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are set
    if (
        "AZURE_CONTENT_SAFETY_ENDPOINT" not in os.environ
        or "AZURE_CONTENT_SAFETY_KEY" not in os.environ
    ):
        print(
            "Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables."
        )
    else:
        safety_results = check_log_text_safety(sample_log_messages)
        print("Log Text Safety Check Results:")
        for result in safety_results:
            print(result)
