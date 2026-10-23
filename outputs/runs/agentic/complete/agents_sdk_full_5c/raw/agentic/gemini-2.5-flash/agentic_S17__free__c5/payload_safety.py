from google.cloud import dlp

def check_payload_safety_with_dlp(project_id: str, text_payload: str, info_types: list[str] = None) -> dict:
    """Checks a decrypted text payload for unsafe content using Google Cloud DLP.

    Args:
        project_id: The ID of the GCP project.
        text_payload: The decrypted text content to scan.
        info_types: A list of info types to scan for (e.g., ["EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD_NUMBER"])
                    If None, a default set of common info types will be used.

    Returns:
        A dictionary containing DLP inspection findings.
    """
    client = dlp.DlpServiceClient()
    project_path = f"projects/{project_id}"

    if info_types is None:
        info_types = [
            "CREDIT_CARD_NUMBER",
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "US_SOCIAL_SECURITY_NUMBER",
            "IP_ADDRESS",
            "GENERIC_PII",
            "FINANCIAL_ACCOUNT_NUMBER",
            "MEDICAL_TERM",
            "DATE_OF_BIRTH"
        ]

    # Convert the list of strings to a list of dlp.InfoType objects.
    info_types_objects = [{'name': info_type} for info_type in info_types]

    # Construct the `inspect_config` for the request.
    inspect_config = {
        'info_types': info_types_objects,
        'include_quote': True,
        'min_likelihood': dlp.Likelihood.POSSIBLE.value,
    }

    # Construct the `item` for the request.
    item = {'value': text_payload}

    # Call the API
    response = client.inspect_content(request={
        'parent': project_path,
        'inspect_config': inspect_config,
        'item': item
    })

    findings_summary = []
    if response.result.findings:
        for finding in response.result.findings:
            findings_summary.append({
                "info_type": finding.info_type.name,
                "likelihood": dlp.Likelihood(finding.likelihood).name,
                "quote": finding.quote,
                "start_index": finding.location.byte_range.start,
                "end_index": finding.location.byte_range.end,
            })
    
    return {"findings": findings_summary, "findings_count": len(findings_summary)}

if __name__ == '__main__':
    # Example usage - replace with your actual project ID
    PROJECT_ID = "your-gcp-project-id"
    UNSAFE_PAYLOAD = "My email is test@example.com, and my SSN is 000-00-0000. My credit card is 1111-2222-3333-4444."
    SAFE_PAYLOAD = "This is a safe message with no sensitive information."

    print("\n--- Checking UNSAFE_PAYLOAD ---")
    try:
        results = check_payload_safety_with_dlp(PROJECT_ID, UNSAFE_PAYLOAD)
        import json
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error checking unsafe payload: {e}")

    print("\n--- Checking SAFE_PAYLOAD ---")
    try:
        results = check_payload_safety_with_dlp(PROJECT_ID, SAFE_PAYLOAD)
        import json
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error checking safe payload: {e}")
