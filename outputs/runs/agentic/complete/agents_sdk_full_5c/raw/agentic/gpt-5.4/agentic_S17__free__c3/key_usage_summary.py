from __future__ import annotations

from collections import Counter
from typing import Iterable, List, Optional

from google.cloud import logging_v2

from security_client import GOOGLE_CLOUD_PROJECT
from security_models import KeyUsageSummary


KMS_AUDIT_SERVICE = "cloudkms.googleapis.com"


def key_usage_summary(project_id: Optional[str] = None, limit: int = 100) -> KeyUsageSummary:
    project = project_id or GOOGLE_CLOUD_PROJECT
    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")

    client = logging_v2.Client(project=project)
    logger_filter = (
        'resource.type="audited_resource" '
        f'protoPayload.serviceName="{KMS_AUDIT_SERVICE}"'
    )
    entries: Iterable = client.list_entries(filter_=logger_filter, page_size=limit)

    method_counter: Counter[str] = Counter()
    resources: List[str] = []
    total = 0
    for entry in entries:
        total += 1
        payload = getattr(entry, "payload", {}) or {}
        method = payload.get("methodName", "unknown")
        resource = payload.get("resourceName", "unknown")
        method_counter[method] += 1
        resources.append(resource)

    return KeyUsageSummary(
        total_events=total,
        by_method=dict(method_counter),
        affected_resources=sorted(set(resources)),
    )
