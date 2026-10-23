import os
from typing import List, Dict
import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.environ.get("GCP_LOCATION", "us-central1")

def check_log_text_safety(log_messages: List[str]) -> Dict[str, str]:
    """Checks selected log message text for unsafe content using Google Cloud Generative AI.

    Args:
        log_messages: A list of log message strings to check.

    Returns:
        A dictionary where keys are original log messages and values are safety ratings
        (e.g., 'SAFE', 'UNSAFE', 'REVIEW_REQUIRED') or a brief explanation.
    """
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    model = GenerativeModel("gemini-pro") # Or another suitable model

    if not log_messages:
        return {"status": "No log messages provided for safety check.", "results": {}}

    results = {}
    for i, message in enumerate(log_messages):
        prompt = (
            f"Analyze the following log message for any unsafe content, "
            f"such as PII (Personally Identifiable Information), sensitive data, "
            f"malicious patterns, or inappropriate language. "
            f"Respond with 'SAFE' if no unsafe content is found, or describe the unsafe content found. "
            f"Only provide the safety assessment for the message.\n\nLog Message {i+1}: {message}"
        )
        
        try:
            response = model.generate_content(prompt)
            results[message] = response.text.strip()
        except Exception as e:
            results[message] = f"Error during safety check: {e}"
            
    return {"status": "Completed", "results": results}

if __name__ == '__main__':
    # Example usage
    sample_log_messages = [
        "User 'john.doe@example.com' logged in from 192.168.1.1.",
        "Payment transaction processed successfully for order #XYZ123.",
        "Error: SQL Injection attempt detected with input: ' OR 1=1;--'",
        "DEBUG: Processing sensitive user data from /tmp/user_data.csv.",
        "Application started normally.",
        "User with SSN XXX-XX-1234 performed an action."
    ]

    safety_check_results = check_log_text_safety(sample_log_messages)
    print("\n--- Log Text Safety Check Results ---")
    for msg, result in safety_check_results['results'].items():
        print(f"Message: '{msg}'\nSafety Assessment: {result}\n")
