# [LATER-STEP] moderation_summary.py

import json
from typing import List, Dict


def summarize_decisions(decisions: List[dict]) -> str:
    """Create a concise markdown summary of moderation decisions.

    Expects each decision dict to follow the SAME-scenario output format:
    {
        'unsafe': bool,
        'categories': List[{'name': str, 'severity': int}],
    }
    The summary lists unsafe messages, the detected categories, and highlights
    any repeated issues across the batch.
    """
    unsafe_msgs = [msg for msg in decisions if msg.get('unsafe')]
    if not unsafe_msgs:
        return "All messages passed safety checks."

    summary_lines = ["## Moderation Summary", ""]
    summary_lines.append(f"Detected {len(unsafe_msgs)} unsafe message{'' if len(unsafe_msgs)==1 else 's'} out of {len(decisions)}.\")
    for i, d in enumerate(unsafe_msgs, start=1):
        summary_lines.append(f"### Message {i}\n")
        summary_lines.append(
            f"**Text preview**: {d.get('text', '[preview hidden]')}"
        )
        if d.get('categories'):
            summary_lines.append(
                "**Detected categories**:\n"
                + ", ".join(
                    f"`{c['name']}` (severity {c['severity']})"
                    for c in d['categories']
                )
                + "\n"
            )
        else:
            summary_lines.append("No specific categories reported.\n")
        summary_lines.append("---\n")
    return "\n".join(summary_lines)
