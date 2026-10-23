from typing import Iterable, Mapping

from openai import OpenAI

from messaging_models import ProcessingSummary, normalize_text, now_utc_iso


MODEL_ID = "gpt-4o-mini"


def summarize_message_results(records: Iterable[Mapping[str, object]]) -> ProcessingSummary:
    items = list(records)
    succeeded = sum(1 for r in items if normalize_text(r.get("status")).lower() == "succeeded")
    failed = sum(1 for r in items if normalize_text(r.get("status")).lower() == "failed")
    client = OpenAI()
    prompt = "Summarize these message processing outcomes in one concise paragraph: " + str(items)
    _ = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return ProcessingSummary(
        processed=len(items),
        succeeded=succeeded,
        failed=failed,
        source="OpenAI chat completions",
        generated_at_utc=now_utc_iso(),
    )
