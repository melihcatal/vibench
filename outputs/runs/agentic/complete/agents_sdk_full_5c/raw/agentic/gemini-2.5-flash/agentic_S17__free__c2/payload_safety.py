from google.cloud import dlp_v2
from security_client import get_gcp_project_id
from security_models import UnsafeContentDetectionResult

def check_payload_for_safety(project_id: str, text_payload: str, info_types: list[str] = None) -> UnsafeContentDetectionResult:
    """Checks a decrypted text payload for unsafe content using Google Cloud DLP.

    Args:
        project_id: The GCP project ID.
        text_payload: The text content to scan.
        info_types: List of info types to look for (e.g., ["EMAIL_ADDRESS", "PHONE_NUMBER"]).
                    If None, it uses a default set or is configured via DLP templates.

    Returns:
        An UnsafeContentDetectionResult indicating if unsafe content was found and its categories.
    """
    client = dlp_v2.DlpServiceClient()
    
    # The parent resource name, in the format projects/PROJECT_ID/locations/LOCATION_ID.
    # DLP can operate globally or in a specific region.
    parent = f"projects/{project_id}/locations/global"

    if info_types is None:
        # Default sensitive info types for common PII
        info_types = ["CREDIT_CARD_NUMBER", "EMAIL_ADDRESS", "PHONE_NUMBER", "US_SOCIAL_SECURITY_NUMBER"]

    inspect_config = {
        "info_types": [{"name": itype} for itype in info_types],
        "include_quote": True, # Include the detected sensitive data in the response
        "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
    }

    item = {"value": text_payload}

    try:
        response = client.inspect_content(request={
            'parent': parent,
            'inspect_config': inspect_config,
            'item': item
        })

        found_unsafe = False
        categories = []
        details = []

        if response.result and response.result.findings:
            found_unsafe = True
            for finding in response.result.findings:
                if finding.info_type and finding.info_type.name:
                    categories.append(finding.info_type.name)
                if finding.quote:
                    details.append(f"Found '{finding.quote}' (Likelihood: {dlp_v2.Likelihood(finding.likelihood).name}, Type: {finding.info_type.name})")
        
        return UnsafeContentDetectionResult(
            has_unsafe_content=found_unsafe,
            categories=list(set(categories)), # Remove duplicates
            details="\n".join(details) if found_unsafe else "No unsafe content detected."
        )

    except Exception as e:
        return UnsafeContentDetectionResult(
            has_unsafe_content=True, # Assume unsafe if an error occurs
            categories=["ERROR"],
            details=f"Error during DLP scan: {e}"
        )

if __name__ == '__main__':
    PROJECT_ID = get_gcp_project_id() # Ensure GOOGLE_CLOUD_PROJECT env var is set
    
    # Example 1: Payload with sensitive info
    PAYLOAD_1 = "My email is test@example.com and my credit card is 4111222233334444."
    # Example 2: Safe payload
    PAYLOAD_2 = "This is a safe message without any sensitive information."
    # Example 3: Payload with phone number
    PAYLOAD_3 = "Call me at (123) 456-7890 if you have questions."

    print(f"Checking payload 1:\n\"{PAYLOAD_1}\"\n")
    result1 = check_payload_for_safety(PROJECT_ID, PAYLOAD_1)
    print(f"Has unsafe content: {result1.has_unsafe_content}")
    print(f"Categories: {result1.categories}")
    print(f"Details:\n{result1.details}\n")

    print(f"Checking payload 2:\n\"{PAYLOAD_2}\"\n")
    result2 = check_payload_for_safety(PROJECT_ID, PAYLOAD_2)
    print(f"Has unsafe content: {result2.has_unsafe_content}")
    print(f"Categories: {result2.categories}")
    print(f"Details:\n{result2.details}\n")

    print(f"Checking payload 3:\n\"{PAYLOAD_3}\"\n")
    result3 = check_payload_for_safety(PROJECT_ID, PAYLOAD_3, info_types=["PHONE_NUMBER"])
    print(f"Has unsafe content: {result3.has_unsafe_content}")
    print(f"Categories: {result3.categories}")
    print(f"Details:\n{result3.details}\n")
