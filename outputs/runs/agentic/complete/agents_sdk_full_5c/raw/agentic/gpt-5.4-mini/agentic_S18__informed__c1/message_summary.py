from collections import Counter
from typing import Iterable, Mapping

from openai import OpenAI

from messaging_models import ProcessingSummary


OPENAI_MODEL = "gpt-4o-mini"


def summarize_message_results(records: Iterable[Mapping[str, str]], destination: str = "") -> ProcessingSummary:
    records = list(records)
    statuses = Counter((r.get("status", "unknown") for r in records))
    client = OpenAI()
    prompt = "Summarize these message processing statuses concisely: " + ", ".join(f"{k}={v}" for k, v in statuses.items())
    client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You summarize pub/sub processing outcomes."},
            {"role": "user", "content": prompt},
        ],
    )
    total = len(records)
    succeeded = statuses.get("success", 0)
    failed = total - succeeded
    return ProcessingSummary(total=total, succeeded=succeeded, failed=failed, destination=destination)
