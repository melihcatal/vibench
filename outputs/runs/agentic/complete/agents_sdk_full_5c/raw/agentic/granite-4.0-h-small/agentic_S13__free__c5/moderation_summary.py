from typing import List, Dict

def summarize_moderation(decisions: List[dict]) -> Dict[str, int]:
    """Summarize a list of moderation decisions (each a dict with a 'flagged' bool).

    Args:
        decisions: List of moderation results, each expected to have at least a 'flagged' key.

    Returns:
        A dict with counts: {'total': int, 'unsafe': int, 'safe': int}.
    """
    total = len(decisions)
    unsafe = sum(1 for d in decisions if d.get('flagged'))
    return {'total': total, 'unsafe': unsafe, 'safe': total - unsafe}
