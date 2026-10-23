import os
import re
from observability_client import get_client

# ----------- LATER-STEP IMPLEMENTATION ------------
# GCP Monitoring (managed metrics) via monitoring.googleapis.com
# Provider signal: imported client from google.api_core.monitored_resource

def metric_annotation_safety(metric_type: str, unsafe_pattern: str = r"(?i)(secret|key|token|password)") -> bool:
    """Check free-text metric labels or annotations for unsafe text using GCP Monitoring API.

    Args:
        metric_type: Metric descriptor name.
        unsafe_pattern: Regex pattern to detect unsafe substrings (default detects credential-like terms).

    Returns:
        True if any label or description matches the unsafe pattern, otherwise False. Includes provider marker.
    """
    client = get_client()
    # fetch descriptor metadata
    descriptor = client.get_metric_descriptor(name=f"projects/{os.getenv('GCP_PROJECT')}/metricDescriptors/{metric_type}")
    unsafe = False
    unsafe_text = []
    # inspect description and label descriptors
    if descriptor.description and re.search(unsafe_pattern, descriptor.description):
        unsafe = True
        unsafe_text.append(descriptor.description)
    for label in descriptor.labels:
        if label.description and re.search(unsafe_pattern, label.description):
            unsafe = True
            unsafe_text.append(f"Label {label.key}: {label.description}")
        if label.value_type == label.STRING and label.key and re.search(unsafe_pattern, label.key):
            unsafe = True
            unsafe_text.append(f"Label key '{label.key}' matches pattern")
    return {'metric': metric_type, 'unsafe': unsafe, 'details': unsafe_text, 'provider': 'GCP_MONITORING'}
