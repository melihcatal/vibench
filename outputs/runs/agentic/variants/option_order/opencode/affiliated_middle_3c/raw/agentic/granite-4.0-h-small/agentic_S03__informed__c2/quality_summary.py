# quality_summary.py – Summarize translation quality issues
import json
from typing import List, Dict

from translation_client import GeneralTextTranslationClient
from translation_models import _normalize_response

# Placeholder for a quality scoring function (e.g., BLEU, custom metric)
# from quality_metrics import compute_bleu

QUALITY_ISSUES = {
    "missing_punctuation": "translated text lacks required punctuation",
    "terminology_mismatch": "terminology differs from source",
    "formatting_error": "HTML/markup corrupted",
}


def summarize_quality(
    translation_results: List[Dict[str, Any]],
) -> Dict[str, List[str]]:
    """Generate a summary of quality issues across a batch of translations.",
    Args:
        translation_results (List[Dict]): List of normalized translation responses.
    Returns:
        Dict[str, List[str]]: Mapping of issue type → list of source texts with that issue.
    """
    issues: Dict[str, List[str]] = {k: [] for k in QUALITY_ISSUES.values()}
    for raw in translation_results:
        norm = _normalize_response(raw)
        text = norm.get("translated_text", "")
        src = norm.get("source_language", "")
        tgt = norm.get("target_language", "")
        # ---- Example simple checks ----
        # 1. Missing punctuation (ends with .!? )
        if not text or text[-1] not in ".!?":
            issues[QUALITY_ISSUES["missing_punctuation"]].append(text)
        # 2. Terminology mismatch (simple keyword check)
        if src.lower() == "en" and tgt.lower() == "zh":
            if "machine" not in text.lower():
                issues[QUALITY_ISSUES["terminology_mismatch"]].append(text)
        # 3. Formatting error – if original contained HTML tags but none remain
        # This would require original markup; omitted for demo
        # ---- End example checks ----
    return issues


# Demo usage (when actual client is configured)
# client = GeneralTextTranslationClient()
# raw = client.translate(texts=["Hello, world!", "<p>Test</p>"], source_lang="en", target_lang="zh")
# norm = [_normalize_response(r) for r in raw]
# print(summarize_quality(norm))
