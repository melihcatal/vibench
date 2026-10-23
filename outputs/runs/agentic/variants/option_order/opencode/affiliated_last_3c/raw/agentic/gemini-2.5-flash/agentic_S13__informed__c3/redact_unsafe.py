import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions


def redact_unsafe(text: str):
    endpoint = os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"]
    key = os.environ["AZURE_CONTENT_SAFETY_KEY"]

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    # In a real scenario, you would manage blocklists through the Azure portal or API.
    # For demonstration, we'll assume a blocklist named 'my_blocklist' exists and might contain terms to be redacted.
    # The service will flag if any text matches items in the specified blocklist.
    request = AnalyzeTextOptions(
        text=text,
        block_list_names=[
            "my_blocklist"
        ],  # Assuming 'my_blocklist' is configured in your Content Safety resource
    )

    response = client.analyze_text(request)

    # The Azure Content Safety service doesn't perform redaction directly based on categories.
    # It provides blocklist matching. If a match occurs, you would implement client-side redaction logic.

    if response.block_lists_match:  # Check if any blocklist item was matched
        # For the purpose of this example, we'll indicate if a blocklist match occurred.
        # Actual redaction would involve iterating through response.block_lists_match
        # and replacing the matched text. This is a simplified representation.
        return {
            "original_text": text,
            "redacted": False,
            "blocklist_matched": True,
            "matches": [m.block_list_name for m in response.block_lists_match],
        }
    else:
        return {"original_text": text, "redacted": False, "blocklist_matched": False}
