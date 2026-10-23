import os
from google.cloud import dlp_v2
from security_client import get_dlp_client
from security_models import PayloadSafetyRequest


def check_payload_safety(
    request: PayloadSafetyRequest, info_types: list[str] | None = None
) -> dlp_v2.InspectContentResponse:
    client = get_dlp_client()

    if info_types is None:
        info_types = [
            "CREDIT_CARD_NUMBER",
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "US_SOCIAL_SECURITY_NUMBER",
        ]

    item = {"value": request.content}
    inspect_config = {"info_types": [{"name": it} for it in info_types]}

    # Google Cloud DLP signal: google.cloud.dlp_v2.DlpServiceClient
    # Google Cloud DLP signal: client.inspect_content
    response = client.inspect_content(
        request=dlp_v2.InspectContentRequest(
            parent=f"projects/{request.project_id}",
            inspect_config=inspect_config,
            item=item,
        )
    )
    return response
