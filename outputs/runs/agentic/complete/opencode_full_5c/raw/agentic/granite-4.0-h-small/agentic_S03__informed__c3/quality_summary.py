from __future__ import annotations

import os
import sys
from typing import Any, Dict, List

# Import provider‑specific safety utilities (example from later‑step files)
# For illustration we import a placeholder function that would be defined in a later‑step module.
# If the function is not defined, we create a no‑op stub.
try:
    from unsafe_copy_check import unsafe_patterns_present
except ImportError:

    def unsafe_patterns_present(text: str) -> bool:
        # No‑op implementation – replace with real check
        return False


try:
    from translation_memory_embedding import embed_segment
except ImportError:

    def embed_segment(segment: str) -> bytes:
        # No‑op stub – returns empty bytes
        return b""


try:
    from localized_audio_preview import synthesize_speech
except ImportError:

    def synthesize_speech(text: str) -> bytes:
        # No‑op stub – returns empty bytes
        return b""

# --------------------------------------------------------------------
#  Quality Summary Builder
# --------------------------------------------------------------------


def assess_quality(translated: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Produce a human‑readable summary of translation quality issues.

    The input `translated` is the generic response from any translation provider
    (same shape as TranslateResponse).  The function runs the following optional
    checks in order:
        1️⃣ Unsafe / potentially unsafe content detection
        2️⃣ Translation memory similarity (embedding‑based reuse check)
        3️⃣ Spoken preview generation (optional for UI)

    Returns a list of issue dictionaries that can be displayed to a reviewer.
    """
    issues: List[Dict[str, Any]] = []

    original = translated.get("text", "")
    translated_text = translated.get("translated_text", "")
    src_lang = translated.get("source_lang", "")
    tgt_lang = translated.get("target_lang", "")

    # ----------------------------------------------------------------
    # 1️⃣ Unsafe content check
    # ----------------------------------------------------------------
    if unsafe_patterns_present(translated_text):
        issues.append(
            {
                "type": "unsafe_content",
                "details": f"Potentially unsafe content detected in translation.",
                "original": original,
                "translated": translated_text,
                "source_lang": src_lang,
                "target_lang": tgt_lang,
            }
        )

    # ----------------------------------------------------------------
    # 2️⃣ Translation memory similarity
    # ----------------------------------------------------------------
    # Compute an embedding for the translated segment (could be stored in a TM DB)
    embedding = embed_segment(translated_text)
    # In a full implementation we would compare `embedding` against a vector store
    # and report near‑matches.  Here we just flag any segment longer than 200 chars
    # as “long” which could be a reuse candidate.
    if len(translated_text) > 200:
        issues.append(
            {
                "type": "translation_memory",
                "details": "Segment exceeds typical TM length; consider reusing existing TM entry.",
                "size_bytes": len(embedding),
                "original": original,
                "translated": translated_text,
            }
        )

    # ----------------------------------------------------------------
    # 3️⃣ Audio preview (optional UI helper)
    # ----------------------------------------------------------------
    # Generate a short spoken version of the translated text for reviewer.
    audio_bytes = synthesize_speech(translated_text)
    if audio_bytes:
        issues.append(
            {
                "type": "audio_preview",
                "details": "Audio preview generated – can be played in UI.",
                "audio_bytes": audio_bytes,  # placeholder – store or stream as needed
            }
        )

    return issues


# --------------------------------------------------------------------
#  CLI helper – quick test of the quality summarizer
# --------------------------------------------------------------------
if __name__ == "__main__":
    # Expected JSON payload on stdin, e.g.: {"text":"Hello","translated_text":"Hola","source_lang":"en","target_lang":"es"}
    payload = sys.stdin.read()
    try:
        json_payload = json.loads(payload)
    except Exception:
        print("Invalid JSON payload.", file=sys.stderr)
        sys.exit(1)
    summary = assess_quality(json_payload)
    print(json.dumps({"issues": summary}, indent=2, ensure_ascii=False))
