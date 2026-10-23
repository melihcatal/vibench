from google.cloud import dlp_v2
import os

def check_secret_labels_for_safety(project_id: str, text: str) -> dlp_v2.dlp.InspectContentResponse:
    """
    Checks secret labels and notes for unsafe text using Google Cloud DLP.
    """
    client = dlp_v2.DlpServiceClient()

    # The info_types here define what DLP should look for.
    # This list can be customized based on your compliance needs.
    info_types = [
        {"name": "EMAIL_ADDRESS"},
        {"name": "PHONE_NUMBER"},
        {"name": "CREDIT_CARD_NUMBER"},
        {"name": "US_SOCIAL_SECURITY_NUMBER"},
        {"name": "IP_ADDRESS"},
        {"name": "AUTH_TOKEN"},
        {"name": "GENERIC_WEB_CREDENTIAL"},
        # Add more info_types as needed, e.g., specific cloud credentials
    ]

    # Configure the inspection request
    item = {"value": text}

    inspect_config = {
        "info_types": info_types,
        "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
        "limits": {"max_findings_per_request": 0}, # 0 means no limit
        "include_quote": True,
    }

    # Construct the parent resource path
    parent = f"projects/{project_id}/locations/global"

    try:
        response = client.inspect_content(
            request={"parent": parent, "inspect_config": inspect_config, "item": item}
        )
        return response
    except Exception as e:
        raise RuntimeError(f"Error checking text with Google Cloud DLP: {e}")

if __name__ == '__main__':
    # This is an example of how you might use it.
    # GCP_PROJECT_ID must be set as an environment variable.
    #
    # project_id = os.getenv("GCP_PROJECT_ID")
    # if not project_id:
    #     print("GCP_PROJECT_ID environment variable is not set.")
    # else:
    #     unsafe_text = "This is a secret note. User email: user@example.com. Phone: 123-456-7890. API Key: sk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    #     safe_text = "This is a safe note about secret rotation practices."
    #
    #     try:
    #         print(f"Checking unsafe text: \n'{unsafe_text}'")
    #         response_unsafe = check_secret_labels_for_safety(project_id, unsafe_text)
    #         if response_unsafe.findings:
    #             print("Found sensitive information:")
    #             for finding in response_unsafe.findings:
    #                 print(f"  Info type: {finding.info_type.name}, Likelihood: {dlp_v2.Likelihood(finding.likelihood).name}, Quote: '{finding.quote}'")
    #         else:
    #             print("No sensitive information found in unsafe text.")
    #
    #         print(f"\nChecking safe text: \n'{safe_text}'")
    #         response_safe = check_secret_labels_for_safety(project_id, safe_text)
    #         if response_safe.findings:
    #             print("Found sensitive information:")
    #             for finding in response_safe.findings:
    #                 print(f"  Info type: {finding.info_type.name}, Likelihood: {dlp_v2.Likelihood(finding.likelihood).name}, Quote: '{finding.quote}'")
    #         else:
    #             print("No sensitive information found in safe text.")
    #
    #     except RuntimeError as e:
    #         print(f"DLP check failed: {e}")
    #     except Exception as e:
    #         print(f"An unexpected error occurred: {e}")
    pass
