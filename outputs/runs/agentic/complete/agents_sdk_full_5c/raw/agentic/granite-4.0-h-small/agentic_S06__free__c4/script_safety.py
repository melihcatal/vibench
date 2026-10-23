from google.cloud import dlp_v2 as dlp

def is_unsafe(script: str, min_likelihood: str = "POSSIBLE") -> bool:
    """Check a narration script for unsafe content using Google DLP.
    Returns True if unsafe, False otherwise.
    """
    dlp_client = dlp.DlpServiceClient()
    content_item = dlp.ContentItem(value=script)
    inspect_config = dlp.InspectConfig(
        info_types=[
            dlp.InfoType(name="PROFESSIONAL_DEGREES"),
            dlp.InfoType(name="PERSONAL_INFORMATION"),
        ],
        min_likelihood=dlp.Likelihood[min_likelihood],
    )
    response = dlp_client.inspect_content(request={"inspect_config": inspect_config, "item": content_item})
    return len(response.result.findings) > 0

if __name__ == "__main__":
    sample = "Dear user, we are collecting your SSN and credit card details."
    unsafe = is_unsafe(sample)
    print("Unsafe content detected:", unsafe)
