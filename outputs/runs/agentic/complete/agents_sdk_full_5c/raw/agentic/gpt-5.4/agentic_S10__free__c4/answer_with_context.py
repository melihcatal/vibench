from __future__ import annotations

from model_client import HostedModelClient, ensure_messages
from model_models import InferenceRequest, NormalizedTextResult


def answer_with_context(context: str, question: str) -> NormalizedTextResult:
    client = HostedModelClient()
    request = InferenceRequest(
        model=client.choose_model_family("qa"),
        messages=ensure_messages(context, question),
        temperature=0.1,
        max_tokens=220,
        metadata={"task": "context_qa", "provider": "openai", "model_family": "gpt-4.1-mini"},
    )
    return client.generate(request)
