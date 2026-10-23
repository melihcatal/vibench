from google.cloud import dlp_v2
from google.cloud.dlp_v2.types import ContentItem, InspectConfig
from typing import List

# Google Cloud DLP - provider-identifying signal

def check_payload_safety(project_id: str, text_payload: str, info_types: List[str] = None) -> dlp_v2.InspectContentResponse:
    """Checks decrypted text payloads for unsafe or sensitive content using Google Cloud DLP.
    """
    dlp_client = dlp_v2.DlpServiceClient()

    if info_types is None:
        # Default info types to scan for
        info_types = ["EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD_NUMBER", "US_SOCIAL_SECURITY_NUMBER"]

    # Convert the list of strings to a list of InfoType objects expected by DLP
    inspect_info_types = [{"name": it} for it in info_types]

    item = ContentItem(value=text_payload)

    inspect_config = InspectConfig(
        info_types=inspect_info_types,
        include_quote=True,
    )

    parent = f"projects/{project_id}/locations/global"

    response = dlp_client.inspect_content(
        request={
            "parent": parent,
            "inspect_config": inspect_config,
            "item": item,
        }
    )

    return response

if __name__ == '__main__':
    # Example usage:
    # project_id = "your-gcp-project-id"
    # sensitive_text = "My email is test@example.com and my phone is 123-456-7890."
    #
    # dlp_response = check_payload_safety(project_id, sensitive_text)
    # if dlp_response.result.findings:
    #     print("Sensitive data found!")
    #     for finding in dlp_response.result.findings:
    #         print(f"  Info Type: {finding.info_type.name}, Quote: {finding.quote}")
    # else:
    #     print("No sensitive data found.")
    pass
