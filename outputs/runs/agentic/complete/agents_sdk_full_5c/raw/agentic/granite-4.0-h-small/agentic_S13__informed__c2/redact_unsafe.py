import re
from safety_client import SafetyClient
from safety_models import ModerationRequest, ModerationResponse, Flag

def redact_unsafe(text: str) -> str:
    """Flag unsafe spans in text and replace them with [REDACTED].
    Uses Azure AI Content Safety to obtain flag offsets and then redacts them.
    """
    client = SafetyClient()
    request = ModerationRequest(text=text)
    response: ModerationResponse = client.check_content(request)
    # Collect intervals that should be redacted (start, end) exclusive
    intervals = []
    for flag in response.flags:
        # Assuming flag provides start_char and end_char indices;
        # if not present, skip.
        if hasattr(flag, 'start_char') and hasattr(flag, 'end_char'):
            intervals.append((flag.start_char, flag.end_char))
    # Merge overlapping intervals
    if not intervals:
        return text
    intervals.sort()
    merged = []
    cur_start, cur_end = intervals[0]
    for s, e in intervals[1:]:
        if s <= cur_end:
            cur_end = max(cur_end, e)
        else:
            merged.append((cur_start, cur_end))
            cur_start, cur_end = s, e
    merged.append((cur_start, cur_end))
    # Redact intervals
    redacted = []
    last_idx = 0
    for start, end in merged:
        redacted.append(text[last_idx:start])
        redacted.append('[REDACTED]')
        last_idx = end
    redacted.append(text[last_idx:])
    return ''.join(redacted)
