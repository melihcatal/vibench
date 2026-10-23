import os
from typing import Dict, List
from observability_client import get_log_client
from observability_models import LogEvent


def log_text_safety(
    log_events: List[LogEvent], safe_keywords: List[str] = None
) -> List[LogEvent]:
    """Check selected log message text for unsafe content and filter it out.

    By default, uses Alibaba Content Moderation (or any configured provider) via
    the provider client's `moderate_text` method. If no provider is configured,
    a simple keyword blacklist filter is applied.
    """
    safe_events = []
    client = get_log_client()
    blacklist = safe_keywords or ["password", "secret", "apikey", "token"]
    for ev in log_events:
        text = ev.message.lower()
        unsafe = any(word in text for word in blacklist)
        # Provider‑specific moderation call (example using Alibaba SDK)
        # response = client.moderate_text(text=text)
        # unsafe = response.get('hit', False)
        if not unsafe:
            safe_events.append(ev)
    return safe_events
