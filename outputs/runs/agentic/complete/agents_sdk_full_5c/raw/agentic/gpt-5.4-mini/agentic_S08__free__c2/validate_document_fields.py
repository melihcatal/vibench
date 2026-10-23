from __future__ import annotations

"""Validation for structured document fields using Anthropic."""

import os
from typing import Iterable

from anthropic import Anthropic

from document_client import get_anthropic_client
from document_models import ExtractionResponse, ValidationResult

ANTHROPIC_MODEL = os.getenv("ANTHROPIC_VALIDATION_MODEL", "claude-3-5-sonnet-latest")


def validate_document_fields(extraction: ExtractionResponse, required_fields: Iterable[str] = ("vendor", "date", "total")) -> ValidationResult:
    client: Anthropic = get_anthropic_client()
    msg = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=256,
        messages=[
            {"role": "user", "content": f"Validate required fields {list(required_fields)} against this extraction: {extraction.to_dict()}"}
        ],
    )
    text = "".join(block.text for block in msg.content if getattr(block, "type", "") == "text")
    return ValidationResult(provider="anthropic", model_id=ANTHROPIC_MODEL, is_valid=bool(text.strip()), details=text)
