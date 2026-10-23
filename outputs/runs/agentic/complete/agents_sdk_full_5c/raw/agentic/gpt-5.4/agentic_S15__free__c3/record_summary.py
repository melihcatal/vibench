from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI

from database_models import DocumentRecord


OPENAI_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def summarize_records(records: Iterable[DocumentRecord]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    joined = "\n\n".join(
        f"id={record.id}; partition={record.partition_key}; content={record.content}"
        for record in records
    )
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=f"Summarize these document records for an operator:\n\n{joined}",
    )
    return response.output_text
