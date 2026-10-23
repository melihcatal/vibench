import re
from safety_client import SafetyClient

def redact_unsafe(text: str) -> str:
    """Flag or redact unsafe spans from text using detection categories.
    Returns text where any span marked as 'hate', 'self_harm', 'sexual', 'violence' is replaced with '[REDACTED]'.
    """
    client = SafetyClient()
    response = client.analyze_content(text)
    categories_to_redact = {'hate', 'self_harm', 'sexual', 'violence'}
    # Build a combined regex pattern for all flagged spans (simple approach: replace whole matches)
    unsafe_spans = []
    for cat, score in response['categories'].items():
        if cat in categories_to_redact and score > client.thresholds.get(cat, 0.5):
            # Heuristic: flag entire sentence containing the unsafe phrase
            # For demonstration, we'll replace the whole sentence with a placeholder.
            sentences = re.split(r'(?<=[.!?]) +', text)
            redacted_sentences = []
            for sentence in sentences:
                if any(cat in sentence.lower() for cat in categories_to_redact):
                    redacted_sentences.append('[REDACTED]')
                else:
                    redacted_sentences.append(sentence)
            return ' '.join(redacted_sentences)
    # If no unsafe categories, return original text
    return text
