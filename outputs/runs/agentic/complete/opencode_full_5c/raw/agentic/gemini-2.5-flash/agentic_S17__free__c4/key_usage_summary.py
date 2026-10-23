import os
from typing import List, Dict, Any, Optional
from security_client import SecurityClient
from security_models import KeyUsageSummaryRequest, KeyUsageSummaryResponse


def summarize_key_usage(request: KeyUsageSummaryRequest) -> KeyUsageSummaryResponse:
    client = SecurityClient()
    log_entries, next_page_token = client.list_log_entries_with_gcp_logging(
        project_id=request.project_id,
        filter=request.filter,
        page_size=request.page_size,
        page_token=request.page_token,
    )
    return KeyUsageSummaryResponse(
        log_entries=log_entries, next_page_token=next_page_token
    )
