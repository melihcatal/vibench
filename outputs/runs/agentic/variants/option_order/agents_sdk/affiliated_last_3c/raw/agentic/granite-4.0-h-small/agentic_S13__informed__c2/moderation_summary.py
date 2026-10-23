from safety_models import ModSafetyResponse
from typing import TypedDict

# -------------------------------------------------
# Summarize moderation decisions
# -------------------------------------------------
ModerationSummary = TypedDict('ModerationSummary', {
    'text': str,
    'unsafe': bool,
    'reasons': list[str],
    'scores': dict,
})

def moderation_summary(raw_resp: ModSafetyResponse) -> ModerationSummary:
    """Create a concise moderation summary from the raw provider response.
    The summary includes whether the text was flagged as unsafe, the primary reasons,
    and the raw category scores for downstream case handling.
    """
    data = raw_resp['raw_response']['data']
    unsafe = data.get('unsafe', False)
    reasons = data.get('unsafe_reasons', [])
    scores = data.get('scores', {})
    return {'text': raw_resp['raw_response'].get('text'), 'unsafe': unsafe,
            'reasons': reasons, 'scores': scores}

__all__ = ['ModerationSummary', 'moderation_summary']
