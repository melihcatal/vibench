import os
import requests
import json
from typing import Dict, Any, List

def check_text_safety(text_content: str) -> Dict[str, Any]:
    """
    Checks user-generated document fields for unsafe content using Azure AI Content Safety.
    Requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables.
    """
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        return {"status": "error", "message": "Azure Content Safety credentials not set."}

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-04-30-preview"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text_content,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for HTTP errors
        result = response.json()
        return {"status": "success", "analysis": result}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Request to Azure Content Safety failed: {e}"}
    except json.JSONDecodeError:
        return {"status": "error", "message": "Failed to parse JSON response from Azure Content Safety."}


def check_document_fields_safety(document: Dict[str, Any], fields_to_check: List[str]) -> Dict[str, Any]:
    """
    Checks specified fields within a document for unsafe content.
    """
    safety_results = {}
    for field in fields_to_check:
        if field in document and isinstance(document[field], str):
            safety_results[field] = check_text_safety(document[field])
        else:
            safety_results[field] = {"status": "skipped", "message": "Field not found or not a string."}
    return safety_results

if __name__ == '__main__':
    # Example usage (requires AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY to be set up)
    sample_document = {
        "id": "doc_001",
        "user_comment": "This is a great product! I love it.",
        "review_text": "Some users might find this offensive due to its violent imagery."
    }
    fields = ["user_comment", "review_text"]
    results = check_document_fields_safety(sample_document, fields)
    print(f"Content Safety Results: {results}")

    sample_unsafe_text = "I hate everyone! You are all stupid!"
    single_text_result = check_text_safety(sample_unsafe_text)
    print(f"Single Text Safety Result: {single_text_result}")
