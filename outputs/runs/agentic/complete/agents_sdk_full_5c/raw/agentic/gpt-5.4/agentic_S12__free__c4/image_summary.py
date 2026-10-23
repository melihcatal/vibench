from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from vision_models import compact_text_list, top_label_names


PROVIDER = "local_summary_pipeline"


def image_summary(labels: Optional[Iterable[Dict[str, object]]] = None, description: Optional[Dict[str, str]] = None, ocr_blocks: Optional[Iterable[Dict[str, object]]] = None, safety: Optional[Dict[str, object]] = None) -> Dict[str, object]:
    label_names = top_label_names(labels or [], limit=8)
    ocr_text = compact_text_list(block.get("text", "") for block in (ocr_blocks or []))[:5]
    safety_flags: List[str] = []
    for category in (safety or {}).get("categories", []):
        likelihood = str(category.get("likelihood", "")).upper()
        if likelihood in {"LIKELY", "VERY_LIKELY", "POSSIBLE"}:
            safety_flags.append(str(category.get("name", "")))
    parts: List[str] = []
    if description and description.get("text"):
        parts.append(description["text"].strip())
    if label_names:
        parts.append("Key labels: " + ", ".join(label_names) + ".")
    if ocr_text:
        parts.append("Visible text: " + " | ".join(ocr_text) + ".")
    if safety_flags:
        parts.append("Safety review flagged: " + ", ".join(compact_text_list(safety_flags)) + ".")
    return {
        "provider": PROVIDER,
        "summary": " ".join(parts).strip(),
        "labels": label_names,
        "ocr_text": ocr_text,
        "safety_flags": compact_text_list(safety_flags),
    }
