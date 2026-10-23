"""Check localized copy for unsafe content."""

from typing import List, Dict, Any

# Provider identifiers (choose one concrete service)
PROVIDER_NAME = "Azure AI Content Safety"  # <provider>
PROVIDER_SDK = "azure-ai-contentsafety"

# ---------------------------------------------------------------------------
# Simple placeholder implementation – in a real deployment you would initialize
# the Azure Content Safety SDK (or REST client) with credentials and call the
# moderation endpoint.
# ---------------------------------------------------------------------------

# Example of what an actual import would look like (uncomment and configure when
# deploying to production):
# from azure.ai.contentsafety import ContentSafetyClient
# from azure.identity import DefaultAzureCredential
# client = ContentSafetyClient(endpoint=os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT"), credential=DefaultAzureCredential())


def unsafe_copy_check(texts: List[str]) -> List[Dict[str, Any]]:
    """Flag any unsafe localized copy.

    Parameters:
        texts: list of translated strings to be inspected.
    Returns:
        List of dictionaries, each containing:
            - 'text': input string
            - 'unsafe': True if unsafe, False otherwise
            - 'reason': short reason (if unsafe)
    """
    # Placeholder stub: mark every string containing the word 'error' as unsafe.
    results = []
    for txt in texts:
        unsafe = "error" in txt.lower()
        reason = "Contains flagged keyword." if unsafe else "Safe"
        results.append({"text": txt, "unsafe": unsafe, "reason": reason})
    return results


# Demo when executed directly
if __name__ == "__main__":
    sample_texts = [
        "All systems operational.",
        "Please fix this error.",
        "No issues here.",
    ]
    print("Unsafe copy check results:", unsafe_copy_check(sample_texts))
