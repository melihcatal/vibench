from __future__ import annotations

from document_client import load_config, invoke_bedrock_text


def invoice_note_translate(note_text: str, target_language: str = "en") -> str:
    cfg = load_config()
    prompt = (
        f"Translate the following invoice note into {target_language}. Preserve meaning and keep names, amounts, and codes unchanged. "
        f"Text: {note_text}"
    )
    return invoke_bedrock_text(cfg.translation_model_id, prompt)
