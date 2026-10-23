```python
# reviewer_brief_audio.py
# LATER-STEP: Generate spoken briefs for moderation reviewers

# Placeholder: integrate with a TTS provider (e.g., AWS Polly, Azure Speech)
# Demo simply prints what would be spoken

def generate_spoken_brief(decision: Dict[str, Any]) -> None:
    """Create an audio brief for a moderation decision.

    decision should contain fields like 'allow', 'categories', 'reasons'.
    This demo logs the brief text that a TTS service would produce.
    """
    # Build a spoken description
    parts = []
    if decision.get('allow'):
        parts.append("The content is approved.")
    else:
        parts.append("The content was flagged.")
        categories = decision.get('categories', [])
        if categories:
            parts.append(f"Detected unsafe categories: {', '.join(categories)}.")
        reasons = decision.get('reasons', [])
        if reasons:
            parts.append(f"Reasons: {', '.join(reasons)}.")
    brief = ' '.join(parts)
    print(f"[AUDIO BRIEF] [{decision.get('decision_id','N/A')}] {brief} (demo)")
```