from __future__ import annotations

"""Expense normalization with OpenAI structured outputs."""

import os

from openai import OpenAI

from document_client import get_openai_client
from document_models import ExtractionResponse, NormalizedExpense, normalize_expense_payload

OPENAI_MODEL = os.getenv("OPENAI_EXPENSE_MODEL", "gpt-4.1-mini")


def normalize_expense(extraction: ExtractionResponse) -> NormalizedExpense:
    client: OpenAI = get_openai_client()
    prompt = normalize_expense_payload(extraction.to_dict())
    result = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": "Normalize extracted expense data into a standard JSON schema."},
            {"role": "user", "content": prompt},
        ],
    )
    return NormalizedExpense.from_json(result.output_text, provider="openai", model_id=OPENAI_MODEL)
