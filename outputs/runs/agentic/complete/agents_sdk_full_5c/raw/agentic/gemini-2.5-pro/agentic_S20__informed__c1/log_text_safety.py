
import os
from typing import List

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory

def check_log_safety(log_message: str) -> List[dict]:
    """
    Checks a given log message for unsafe content using Azure AI Content Safety.

    Args:
        log_message: The text from a log file to be analyzed.

    Returns:
        A list of dictionaries, each indicating a category and its severity level.
    """
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    if not endpoint or not key:
        raise ValueError("Azure Content Safety credentials are not set in environment variables.")

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=log_message)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text failed: {e}")
        return []

    results = []
    if response.hate_result:
        results.append({"category": TextCategory.HATE, "severity": response.hate_result.severity})
    if response.self_harm_result:
        results.append({"category": TextCategory.SELF_HARM, "severity": response.self_harm_result.severity})
    if response.sexual_result:
        results.append({"category": TextCategory.SEXUAL, "severity": response.sexual_result.severity})
    if response.violence_result:
        results.append({"category": TextCategory.VIOLENCE, "severity": response.violence_result.severity})

    return results

if __name__ == '__main__':
    # Example log messages
    safe_log = "User 1234 successfully updated their profile."
    unsafe_log = "User input contains threatening language: 'I will find you and hurt you.'" # Example of unsafe content

    print(f"Checking safe log: '{safe_log}'")
    safety_analysis_safe = check_log_safety(safe_log)
    if any(r['severity'] > 0 for r in safety_analysis_safe):
        print("Unsafe content detected in safe log:", safety_analysis_safe)
    else:
        print("Safe log is considered safe.")

    print("\n" + "="*20 + "\n")

    print(f"Checking unsafe log: '{unsafe_log}'")
    safety_analysis_unsafe = check_log_safety(unsafe_log)
    if any(r['severity'] > 0 for r in safety_analysis_unsafe):
        print("Unsafe content detected in unsafe log:", safety_analysis_unsafe)
    else:
        print("Unsafe log was not flagged (this is unexpected).")
