import os
import re
from typing import Dict

# Later-step text safety check using an external content moderation service (Alibaba Content Moderation SDK)

# Alibaba Cloud credentials
ALIBABA_ACCESS_KEY_ID = os.getenv('ALIBABA_ACCESS_KEY_ID')
ALIBABA_ACCESS_KEY_SECRET = os.getenv('ALIBABA_ACCESS_KEY_SECRET')
if not (ALIBABA_ACCESS_KEY_ID and ALIBABA_ACCESS_KEY_SECRET):
    raise RuntimeError('Missing Alibaba Cloud credentials')

# Simple moderation wrapper (using SDK placeholder)
def is_metric_label_safe(label_value: str) -> bool:
    """Check a free‑text metric label/annotation for unsafe content using Alibaba Cloud Content Moderation.",
    """Returns True if the label passes moderation, False otherwise.",
    """
    # Placeholder for actual SDK call; in real code you would import alibabacloud_green and use its API.
    # Here we simulate with a basic regex filter for profanity.
    profanity_pattern = re.compile(r'\b(?:badword1|badword2)\b', re.IGNORECASE)
    return not profanity_pattern.search(label_value)
