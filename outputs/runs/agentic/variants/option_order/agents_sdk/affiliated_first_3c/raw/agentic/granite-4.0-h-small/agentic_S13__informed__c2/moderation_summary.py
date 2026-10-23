# [LATER-STEP] moderation_summary.py

from typing import List, Dict

from safety_models import TextModerationResult, UnsafeSpan

SUMMARY_FIELDS = ['category', 'score', 'threshold']

def summarize_moderation(results: List[TextModerationResult]) -> str:
    """Create a concise human‑readable summary of moderation decisions.
    Returns a multi‑line string, one section per text.
    """
    lines = []
    for idx, result in enumerate(results, start=1):
        lines.append(f\"=== Moderation Result {idx} ===\")
        lines.append(f\"Text: {result} (decision: {result.decision})\")
        for cat, score in result.detailed.items():
            lines.append(f\"  {cat.upper()}: score={score:.3f}, threshold={result.thresholds.get(cat,0.5):.3f}\")
        unsafe_spans: List[UnsafeSpan] = getattr(result, 'unsafe_spans', [])
        if unsafe_spans:
            lines.append('  FLAGGED SPANS:')
            for span in unsafe_spans:
                lines.append(f\"    [{span.category}] [{span.start}:{span.end}] score={span.score:.3f}\")
        else:
            lines.append('  No unsafe spans detected.')\n        lines.append('')\n    return '\\n'.join(lines)
