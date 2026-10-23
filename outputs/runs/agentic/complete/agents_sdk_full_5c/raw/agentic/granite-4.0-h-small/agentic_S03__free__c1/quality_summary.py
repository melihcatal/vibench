# [LATER-STEP] quality_summary.py
from typing import List

def summarize_quality(translation_results: List[str], source_texts: List[str]) -> str:
    """Provide a simple summary of translation quality issues."""
    issues = []
    for src, tgt in zip(source_texts, translation_results):
        if not tgt or tgt.strip() == src.strip():
            issues.append('Potential translation failure or no change detected.')
        elif len(tgt) < 0.5 * len(src):
            issues.append('Output is unusually short relative to source.')
    summary = 'Translation quality check found ' + str(len(issues)) + ' issue(s).\n' + '\n'.join(['- ' + i for i in issues])
    return summary if issues else 'No quality issues detected.'
