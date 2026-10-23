from google.cloud import dlp_v2
import os

def check_payload_safety(project_id: str, text_payload: str, info_types: list[str] = None) -> dict:
    """Checks decrypted text payloads for unsafe content using Google Cloud DLP.

    Args:
        project_id: Your Google Cloud project ID.
        text_payload: The decrypted text payload to scan.
        info_types: A list of info types to scan for (e.g., ["EMAIL_ADDRESS", "PHONE_NUMBER"]).
                    If None, a default set of common info types will be used.

    Returns:
        A dictionary containing the DLP inspection results.
    """
    dlp_client = dlp_v2.DlpServiceClient()
    project_path = f"projects/{project_id}"

    if info_types is None:
        info_types = ["CREDIT_CARD_NUMBER", "EMAIL_ADDRESS", "PHONE_NUMBER", "US_SOCIAL_SECURITY_NUMBER"]

    # Convert info_types list to DlpV2InfoType objects
    inspect_info_types = [{"name": itype} for itype in info_types]

    item = {"value": text_payload}

    inspect_config = {
        "info_types": inspect_info_types,
        "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
        "limits": {"max_findings_per_request": 0} # 0 means no limit
    }

    try:
        response = dlp_client.inspect_content(
            request={
                "parent": project_path,
                "inspect_config": inspect_config,
                "item": item,
            }
        )
        findings = []
        if response.result and response.result.findings:
            for finding in response.result.findings:
                findings.append({
                    "info_type": finding.info_type.name,
                    "likelihood": dlp_v2.Likelihood(finding.likelihood).name,
                    "quote": finding.quote,
                })
        return {"findings": findings, "success": True}

    except Exception as e:
        return {"error": str(e), "success": False}
