# [LATER-STEP] quality_summary.py
"""Summarize translation quality issues after processing translated texts.
Provides a high‑level report of problematic segments, missing translations,
and length mismatches."

from __future__ import annotations
from typing import List, Dict, Any
import json

# Simple contract for a translated segment
TranslatedSegment = Dict[str, Any]

# ---------------------------------------------------------------------------
# Issue taxonomy (extend as needed)
# ---------------------------------------------------------------------------

ISSUE_TYPES = [
    "missing_translation",
    "length_mismatch",
    "placeholder_mismatch",
    "syntax_error",
]

def _classify_issue(segment: TranslatedSegment) -> str:
    """Heuristic classification of a single segment.
    Returns one of ISSUE_TYPES or None if no obvious issue."
    """
    if not segment.get("translated_text"):
        return "missing_translation"
    src_len = len(segment.get("source_text", ""))
    tgt_len = len(segment.get("translated_text", ""))
    if abs(src_len - tgt_len) > 0.3 * src_len:
        return "length_mismatch"
    # Placeholder check: assume placeholders look like {0}, {name}
    src_placeholders = len(set(filter(lambda x: x.startswith('{'), segment.get("source_text", ""))))
    tgt_placeholders = len(set(filter(lambda x: x.startswith('{'), segment.get("translated_text", ""))))
    if src_placeholders != tgt_placeholders:
        return "placeholder_mismatch"
    # Very naive syntax error detection (missing closing bracket)
    if seg := segment.get("translated_text"):
        if seg.count('(') != seg.count(')') or seg.count('[') != seg.count(']'):
            return "syntax_error"
    return None

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def summarize(translations: List[TranslatedSegment]) -> Dict[str, Any]:
    """Produce a report summarizing quality checks.

    Args:
        translations: List of translated segment dicts, each containing at
                      least 'source_text' and 'translated_text' keys.

    Returns:
        A dict with overall counts and a breakdown per issue type.
    """
    report: Dict[str, Any] = {
        "total_segments": len(translations),
        "issues": {t: 0 for t in ISSUE_TYPES},
        "segment_examples": []
    }
    for seg in translations:
        issue = _classify_issue(seg)
        if issue:
            report["issues"][issue] += 1
            # Keep a few examples for human review
            if len(report["segment_examples"]) < 5:
                report["segment_examples"].append(seg)
    return report

# ---------------------------------------------------------------------------
# CLI entry point (optional, for debugging)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse, sys
    parser = argparse.ArgumentParser(description="Parse JSON of translated segments and output quality summary.")
    parser.add_argument("input_file", type=str, help="Path to JSON file containing list of segment dicts.")
    args = parser.parse_args()
    with open(args.input_file) as f:
        data = json.load(f)
    summary = summarize(data)
    print(json.dumps(summary, indent=2))