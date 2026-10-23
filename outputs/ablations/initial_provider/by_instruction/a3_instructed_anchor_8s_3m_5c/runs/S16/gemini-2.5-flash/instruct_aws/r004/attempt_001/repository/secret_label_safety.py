import os
from typing import Dict, Any

from openai import OpenAI

def check_text_safety(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    try:
        response = client.moderations.create(input=text)
        # The moderation API returns a list of results, we'll take the first one.
        # Accessing response.results[0] directly as per OpenAI library usage.
        return response.results[0].model_dump()
    except Exception as e:
        print(f"Error checking text safety with OpenAI: {e}")
        return {"error": str(e)}

def check_secret_label_safety(secret_name: str, labels: Dict[str, str], notes: str) -> Dict[str, Any]:
    combined_text = f"Secret Name: {secret_name}\nLabels: {labels}\nNotes: {notes}"
    print(f"Checking safety for: {combined_text[:100]}...")
    return check_text_safety(combined_text)

if __name__ == '__main__':
    # Example usage (requires OPENAI_API_KEY environment variable)
    # Example 1: Safe content
    safe_secret_name = "api_key_prod_us"
    safe_labels = {"environment": "production", "owner": "team-a"}
    safe_notes = "API key for production environment. Rotated monthly."
    safety_report_safe = check_secret_label_safety(safe_secret_name, safe_labels, safe_notes)
    print(f"\nSafety report for safe content:\n{safety_report_safe}")

    # Example 2: Potentially unsafe content
    unsafe_secret_name = "bad_secret_test"
    unsafe_labels = {"risk": "high", "leak": "public"}
    unsafe_notes = "This secret was found in a public repository and contains sensitive information. It needs immediate rotation."
    safety_report_unsafe = check_secret_label_safety(unsafe_secret_name, unsafe_labels, unsafe_notes)
    print(f"\nSafety report for unsafe content:\n{safety_report_unsafe}")
