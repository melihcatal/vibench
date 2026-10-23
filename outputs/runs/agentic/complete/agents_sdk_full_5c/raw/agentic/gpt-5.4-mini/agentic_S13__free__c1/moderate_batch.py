from __future__ import annotations

import json
from typing import Iterable, List

from safety_client import get_openai_client, safety_model_name
from safety_models import ModerationBatchRequest, ModerationBatchResult, normalize_batch_response


BATCH_SYSTEM_PROMPT = """You are a text moderation engine.\nFor each input message, return a JSON array of decision objects with fields: index, allowed, categories, reasons.\n"""


def moderate_batch(messages: Iterable[str]) -> ModerationBatchResult:
    request = ModerationBatchRequest(messages=list(messages))
    client = get_openai_client()
    completion = client.responses.create(  # openai SDK
        model=safety_model_name("batch_moderation"),
        input=[
            {"role": "system", "content": BATCH_SYSTEM_PROMPT},
            {"role": "user", "content": request.to_prompt()},
        ],
        temperature=0,
    )
    return normalize_batch_response(completion)
