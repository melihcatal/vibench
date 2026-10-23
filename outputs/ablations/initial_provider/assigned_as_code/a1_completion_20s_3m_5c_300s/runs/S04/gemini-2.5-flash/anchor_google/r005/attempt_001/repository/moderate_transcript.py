from google.cloud import dlp_v2 as dlp
from speech_models import ModerationRequest, ModerationResult

def moderate_transcript(request: ModerationRequest, project_id: str) -> ModerationResult:
    client = dlp.DlpServiceClient()
    # Construct the `inspect_config` to specify the types of content to scan
    # For moderation, we can use built-in info types or custom ones.
    # Here, we'll use a few common ones as an example.
    inspect_config = {
        "info_types": [
            {"name": "EMAIL_ADDRESS"},
            {"name": "PHONE_NUMBER"},
            {"name": "CREDIT_CARD_NUMBER"},
            {"name": "US_SOCIAL_SECURITY_NUMBER"},
        ],
        "include_quote": True,
    }
    
    # Optionally, you can add custom dictionaries for specific inappropriate words
    # For simplicity, we'll stick to built-in info types for now.

    # The item to be inspected.
    item = {"value": request.text}

    # Convert the project id into a full resource name.
    parent = f"projects/{project_id}"

    response = client.inspect_content(request={
        "parent": parent,
        "inspect_config": inspect_config,
        "item": item,
    })

    findings = response.result.findings
    is_safe = True
    scores = {"matches_found": len(findings)}

    if findings:
        is_safe = False

    return ModerationResult(is_safe=is_safe, scores=scores)
