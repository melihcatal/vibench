import os
from google.cloud import dlp_v2
from security_models import DlpScanRequest, DlpScanResponse
from typing import List, Dict, Any


def check_payload_safety(request: DlpScanRequest) -> DlpScanResponse:
    """
    Checks decrypted text payloads for unsafe content using Google Cloud Data Loss Prevention (DLP).
    """
    dlp_client = dlp_v2.DlpServiceClient()

    item = {"value": request.text_content}

    inspect_config = {
        "info_types": [{"name": info_type} for info_type in request.info_types],
        "min_likelihood": request.min_likelihood,
    }

    # Construct the `parent` argument for the request
    parent = f"projects/{request.project_id}/locations/global"  # Or specific location

    response = dlp_client.inspect_content(
        request={"parent": parent, "inspect_config": inspect_config, "item": item}
    )

    findings_list: List[Dict[str, Any]] = []
    if response.result.findings:
        for finding in response.result.findings:
            findings_list.append(
                {
                    "info_type": finding.info_type.name,
                    "likelihood": finding.likelihood.name,
                    "quote": finding.quote,
                    "start_index": finding.location.content_bytes_range.start,
                    "end_index": finding.location.content_bytes_range.end,
                }
            )

    return DlpScanResponse(findings=findings_list)


if __name__ == "__main__":
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")

    if PROJECT_ID == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        sample_unsafe_payload = "My email is test@example.com and my phone number is 123-456-7890. My SSN is 999-99-9999."

        dlp_request = DlpScanRequest(
            text_content=sample_unsafe_payload,
            project_id=PROJECT_ID,
            info_types=["EMAIL_ADDRESS", "PHONE_NUMBER", "US_SOCIAL_SECURITY_NUMBER"],
            min_likelihood="POSSIBLE",
        )

        print("Checking payload for unsafe content...")
        dlp_response = check_payload_safety(dlp_request)

        if dlp_response.findings:
            print("Unsafe content found:")
            for finding in dlp_response.findings:
                print(
                    f"  Info Type: {finding['info_type']}, Likelihood: {finding['likelihood']}, Quote: '{finding['quote']}'"
                )
        else:
            print("No unsafe content found.")
