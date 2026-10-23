import os
from safety_models import SafetyModels

def moderation_summary(decisions: list[dict]) -> str:
    """Summarize moderation decisions for a batch of messages.
    Returns a concise human-readable summary indicating which messages passed and which failed, and why.
    """
    summary_lines = []
    for i, decision in enumerate(decisions, start=1):
        status = 'SAFE' if decision['safe'] else 'UNSAFE'
        unsafe_cats = [cat for cat, score in decision['categories'].items() if score > 0.5]
        if unsafe_cats:
            details = f' flagged for: {', '.join(unsafe_cats)}'
        else:
            details = ''
        summary_lines.append(f'Message {i}: {status}{details}')
    return '\n'.join(summary_lines)

# Example usage (not executed)
# decisions = moderate_batch(['Hello', 'This is a hate statement.'])
# print(moderation_summary(decisions))
