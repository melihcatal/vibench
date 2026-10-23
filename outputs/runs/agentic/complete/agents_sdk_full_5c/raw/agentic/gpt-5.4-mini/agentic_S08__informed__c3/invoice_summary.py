from __future__ import annotations

from document_client import load_config, invoke_bedrock_text


def invoice_summary(extracted_invoice: dict) -> str:
    cfg = load_config()
    prompt = (
        "Summarize the following extracted invoice JSON in 2-3 sentences, mentioning vendor, total, and notable line items. "
        f"Invoice JSON: {extracted_invoice}"
    )
    return invoke_bedrock_text(cfg.summary_model_id, prompt)
